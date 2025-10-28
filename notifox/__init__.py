from .client import NotifoxClient
from .exceptions import (
    NotifoxAPIError,
    NotifoxAuthenticationError,
    NotifoxConnectionError,
    NotifoxError,
    NotifoxRateLimitError,
)

__all__ = [
    "NotifoxClient",
    "NotifoxError",
    "NotifoxAPIError",
    "NotifoxAuthenticationError",
    "NotifoxRateLimitError",
    "NotifoxConnectionError",
]
__version__ = "0.1.1"
