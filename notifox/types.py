# notifox/types.py
"""Channel types for Notifox alerts."""


class Channel:
    """Base class for channel types."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value


# Channel type constants
SMS = Channel("sms")
Email = Channel("email")
