# notifox-py

Python SDK for [Notifox](https://notifox.com).

## Installation

```bash
pip install notifox
```

## Usage

```python
from notifox import NotifoxClient

client = NotifoxClient(api_key="your_api_key_here")
client.send_alert(audience="mike", alert="Database server is down!")
```

Or use the environment variable:

```bash
export NOTIFOX_API_KEY="your_api_key_here"
```

```python
client = NotifoxClient()  # Reads from NOTIFOX_API_KEY
client.send_alert(audience="mike", alert="High CPU usage!")
```

### Configuration

```python
client = NotifoxClient(
    api_key="your_api_key",
    base_url="https://api.notifox.com",
    timeout=30.0,
    max_retries=3
)
```

## Error Handling

```python
from notifox import (
    NotifoxClient,
    NotifoxAuthenticationError,
    NotifoxRateLimitError,
    NotifoxAPIError,
    NotifoxConnectionError
)

try:
    client.send_alert(audience=["admin"], alert="Alert")
except NotifoxAuthenticationError:
    pass
except NotifoxRateLimitError:
    pass
except NotifoxAPIError as e:
    print(f"{e.status_code}: {e.response_text}")
```

Available exceptions:
- `NotifoxError` - Base exception
- `NotifoxAuthenticationError` - Authentication failed (401/403)
- `NotifoxRateLimitError` - Rate limit exceeded (429)
- `NotifoxAPIError` - General API errors
- `NotifoxConnectionError` - Network errors