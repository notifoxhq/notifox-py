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

## Calculate parts

When you send a message, the length and characters dictate how many parts you will be charged for. You can read more about calculating the parts [here](https://docs.notifox.com/docs/reference/parts).

The Notifox Alerts API exposes a route that lets you calculate the amount of parts a message will be without sending the alert.

```python
from notifox import NotifoxClient

client = NotifoxClient()

# Calculate the parts of the alert
response = client.calculate_parts(
    alert="Hello, world!"
)

# {'parts': 1, 'cost': 0.025, 'currency': 'USD', 'encoding': 'GSM-7', 'characters': 22, 'message': 'Notifox: Hello, world!'}
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

client = NotifoxClient(api_key="your_api_key")

try:
    client.send_alert(audience="admin", alert="System is running low on memory")
except NotifoxAuthenticationError:
    print("Authentication failed. Check your API key.")
except NotifoxRateLimitError:
    print("Rate limit exceeded. Please wait before sending more alerts.")
except NotifoxAPIError as e:
    print(f"API error ({e.status_code}): {e.response_text}")
except NotifoxConnectionError as e:
    print(f"Connection failed: {e}")
```

Available exceptions:
- `NotifoxError` - Base exception
- `NotifoxAuthenticationError` - Authentication failed (401/403)
- `NotifoxRateLimitError` - Rate limit exceeded (429)
- `NotifoxAPIError` - General API errors
- `NotifoxConnectionError` - Network errors