# notifox/client.py
import os
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    NotifoxAPIError,
    NotifoxAuthenticationError,
    NotifoxConnectionError,
    NotifoxError,
    NotifoxRateLimitError,
)


class NotifoxClient:
    """
    Python SDK for Notifox alerting API.

    Examples:
        client = NotifoxClient(api_key="your_api_key")
        client.send_alert(audience="user1", alert="Server down!")

        client = NotifoxClient()  # Reads from NOTIFOX_API_KEY env var
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.notifox.com",
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        """
        Initialize the Notifox client.

        Args:
            api_key: Your Notifox API key. If not provided, will attempt to read from
                     the NOTIFOX_API_KEY environment variable.
            base_url: Base URL for the Notifox API. Defaults to https://api.notifox.com
            timeout: Request timeout in seconds. Defaults to 30.0
            max_retries: Maximum number of retries for failed requests. Defaults to 3
        """
        self.api_key = api_key or os.getenv("NOTIFOX_API_KEY")
        if not self.api_key:
            raise NotifoxError(
                "API key is required. Provide it as an argument or set the "
                "NOTIFOX_API_KEY environment variable."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # Create a session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions for errors.

        Args:
            response: The HTTP response from the API

        Returns:
            The JSON response data

        Raises:
            NotifoxAuthenticationError: For 401 or 403 status codes
            NotifoxRateLimitError: For 429 status code
            NotifoxAPIError: For other error status codes
        """
        if response.status_code == 401 or response.status_code == 403:
            raise NotifoxAuthenticationError(
                f"Authentication failed: {response.status_code}",
                status_code=response.status_code,
                response_text=response.text
            )

        if response.status_code == 429:
            raise NotifoxRateLimitError(
                "Rate limit exceeded. Please try again later.",
                status_code=response.status_code,
                response_text=response.text
            )

        if response.status_code >= 400:
            raise NotifoxAPIError(
                f"API error: {response.status_code} - {response.text}",
                status_code=response.status_code,
                response_text=response.text
            )

        return response.json()

    def send_alert(
        self,
        audience: str,
        alert: str
    ) -> Dict[str, Any]:
        """
        Sends an alert to the specified audience.

        Args:
            audience: Audience identifier (e.g., mike, devops, support)
            alert: The alert message to send

        Returns:
            API response as a dictionary

        Raises:
            NotifoxAuthenticationError: If authentication fails
            NotifoxRateLimitError: If rate limit is exceeded
            NotifoxAPIError: For other API errors
            NotifoxConnectionError: If there's a connection issue
        """
        url = f"{self.base_url}/alert"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "audience": audience,
            "alert": alert,
        }

        try:
            resp = self.session.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(resp)
        except requests.exceptions.Timeout:
            raise NotifoxConnectionError(
                f"Request timed out after {self.timeout} seconds"
            ) from None
        except requests.exceptions.ConnectionError as e:
            raise NotifoxConnectionError(f"Connection error: {str(e)}") from e
        except requests.exceptions.RequestException as e:
            raise NotifoxError(f"Request failed: {str(e)}") from e
