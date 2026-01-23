# notifox/exceptions.py
from typing import Optional


class NotifoxError(Exception):
    """Base exception for all Notifox SDK errors."""
    pass


class NotifoxAPIError(NotifoxError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_text: str = "",
        error: Optional[str] = None
    ):
        self.status_code = status_code
        self.response_text = response_text
        self.error = error
        super().__init__(message)


class NotifoxAuthenticationError(NotifoxAPIError):
    """Raised when authentication fails (401/403)."""
    pass


class NotifoxValidationError(NotifoxAPIError):
    """Raised when request validation fails (400)."""
    pass


class NotifoxInsufficientBalanceError(NotifoxAPIError):
    """Raised when user has insufficient balance (402)."""
    pass


class NotifoxRateLimitError(NotifoxAPIError):
    """Raised when rate limit is exceeded (429)."""
    pass


class NotifoxServerError(NotifoxAPIError):
    """Raised when a server error occurs (500)."""
    pass


class NotifoxConnectionError(NotifoxError):
    """Raised when there's a connection error to the API."""
    pass
