# notifox/client.py
import json
import os
from typing import Any, Dict, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    NotifoxAPIError,
    NotifoxAuthenticationError,
    NotifoxConnectionError,
    NotifoxError,
    NotifoxInsufficientBalanceError,
    NotifoxRateLimitError,
    NotifoxServerError,
    NotifoxValidationError,
)
from .types import Channel


class NotifoxClient:
    """
    Python SDK for Notifox alerting API.

    Examples:
        import notifox

        client = notifox.NotifoxClient(api_key="your_api_key")
        client.send_alert(audience="user1", alert="Server down!", channel=notifox.SMS)

        client = notifox.NotifoxClient()  # Reads from NOTIFOX_API_KEY env var
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

    def _parse_error_response(self, response: requests.Response) -> tuple[str, Optional[str]]:
        """
        Parse error response to extract error message and error type.

        Args:
            response: The HTTP response from the API

        Returns:
            Tuple of (error_message, error_type)
        """
        error_message = response.text
        error_type = None

        # Try to parse JSON error response
        if response.headers.get("content-type", "").startswith("application/json"):
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and "error" in error_data:
                    error_type = error_data["error"]
                    error_message = error_data.get("description", error_data["error"])
            except (json.JSONDecodeError, ValueError):
                pass

        return error_message, error_type

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions for errors.

        Args:
            response: The HTTP response from the API

        Returns:
            The JSON response data

        Raises:
            NotifoxAuthenticationError: For 401 or 403 status codes
            NotifoxValidationError: For 400 status code (validation errors)
            NotifoxInsufficientBalanceError: For 402 status code
            NotifoxRateLimitError: For 429 status code
            NotifoxServerError: For 500 status code
            NotifoxAPIError: For other error status codes
        """
        if response.status_code == 401 or response.status_code == 403:
            error_message, _ = self._parse_error_response(response)
            raise NotifoxAuthenticationError(
                error_message or f"Authentication failed: {response.status_code}",
                status_code=response.status_code,
                response_text=response.text
            )

        if response.status_code == 400:
            error_message, error_type = self._parse_error_response(response)
            raise NotifoxValidationError(
                error_message or "Request validation failed",
                status_code=response.status_code,
                response_text=response.text,
                error=error_type
            )

        if response.status_code == 402:
            error_message, error_type = self._parse_error_response(response)
            raise NotifoxInsufficientBalanceError(
                error_message or "Insufficient balance",
                status_code=response.status_code,
                response_text=response.text,
                error=error_type
            )

        if response.status_code == 429:
            error_message, error_type = self._parse_error_response(response)
            raise NotifoxRateLimitError(
                error_message or "Rate limit exceeded. Please try again later.",
                status_code=response.status_code,
                response_text=response.text,
                error=error_type
            )

        if response.status_code >= 500:
            error_message, error_type = self._parse_error_response(response)
            raise NotifoxServerError(
                error_message or "Internal server error",
                status_code=response.status_code,
                response_text=response.text,
                error=error_type
            )

        if response.status_code >= 400:
            error_message, error_type = self._parse_error_response(response)
            raise NotifoxAPIError(
                error_message or f"API error: {response.status_code}",
                status_code=response.status_code,
                response_text=response.text,
                error=error_type
            )

        return response.json()

    def send_alert(
        self,
        audience: str,
        alert: str,
        channel: Optional[Union[Channel, str]] = None
    ) -> Dict[str, Any]:
        """
        Sends an alert to the specified audience.

        Args:
            audience: Audience identifier (e.g., mike, devops, support)
            alert: The alert message to send
            channel: Optional channel type. Use notifox.SMS or notifox.Email,
                    or pass "sms" or "email" as a string. If not provided,
                    the channel will be left blank.

        Returns:
            API response as a dictionary containing message_id and other fields

        Raises:
            NotifoxAuthenticationError: If authentication fails (401/403)
            NotifoxValidationError: If request validation fails (400)
            NotifoxInsufficientBalanceError: If user has insufficient balance (402)
            NotifoxRateLimitError: If rate limit is exceeded (429)
            NotifoxServerError: If a server error occurs (500)
            NotifoxAPIError: For other API errors
            NotifoxConnectionError: If there's a connection issue
        """
        url = f"{self.base_url}/alert"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload: Dict[str, Any] = {
            "audience": audience,
            "alert": alert,
        }

        if channel is not None:
            # Convert Channel object to string, or use string directly
            if isinstance(channel, Channel):
                payload["channel"] = str(channel)
            else:
                payload["channel"] = channel

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

    def calculate_parts(self, alert: str) -> Dict[str, Any]:
        """
        Calculates the parts of the alert.

        Args:
            alert: The alert message to calculate the parts of

        Returns:
            A dictionary containing information about the alert
        """

        url = f"{self.base_url}/alert/parts"
        payload = {
            "alert": alert
        }

        try:
            resp = self.session.post(
                url,
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
        except Exception as e:
            raise NotifoxError("An unknown error occurred") from e
