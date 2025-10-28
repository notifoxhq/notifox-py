# notifox/exceptions.py
class NotifoxError(Exception):
    """Base exception for all Notifox SDK errors."""
    pass


class NotifoxAPIError(NotifoxError):
    """Raised when the API returns an error response."""
    
    def __init__(self, message: str, status_code: int, response_text: str = ""):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)


class NotifoxAuthenticationError(NotifoxAPIError):
    """Raised when authentication fails (401/403)."""
    pass


class NotifoxRateLimitError(NotifoxAPIError):
    """Raised when rate limit is exceeded (429)."""
    pass


class NotifoxConnectionError(NotifoxError):
    """Raised when there's a connection error to the API."""
    pass