from .client import NotifoxClient
from .exceptions import (
    NotifoxError,
    NotifoxAPIError,
    NotifoxAuthenticationError,
    NotifoxRateLimitError,
    NotifoxConnectionError
)

__all__ = [
    "NotifoxClient",
    "NotifoxError",
    "NotifoxAPIError",
    "NotifoxAuthenticationError",
    "NotifoxRateLimitError",
    "NotifoxConnectionError",
]
__version__ = "0.1.0"