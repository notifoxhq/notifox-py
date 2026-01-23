# notifox-py

Python SDK for [Notifox](https://notifox.com).

## Installation

```bash
pip install notifox
```

## Usage

```python
import notifox

client = notifox.NotifoxClient(api_key="your_api_key_here")
client.send_alert(audience="mike", alert="Database server is down!")
```

Or use the environment variable:

```bash
export NOTIFOX_API_KEY="your_api_key_here"
```

```python
import notifox

client = notifox.NotifoxClient()  # Reads from NOTIFOX_API_KEY
client.send_alert(audience="mike", alert="High CPU usage!")
```

### Channel Selection

You can optionally specify a channel (SMS or email):

```python
import notifox

client = notifox.NotifoxClient()

# Send via SMS
response = client.send_alert(
    audience="mike",
    alert="Server is down!",
    channel=notifox.SMS
)

# Send via email
response = client.send_alert(
    audience="mike",
    alert="Server is down!",
    channel=notifox.Email
)

# If channel is not specified, it will be left blank
response = client.send_alert(
    audience="mike",
    alert="Server is down!"
)
```

### Configuration

```python
import notifox

client = notifox.NotifoxClient(
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
import notifox

client = notifox.NotifoxClient()

# Calculate the parts of the alert
response = client.calculate_parts(
    alert="Hello, world!"
)

# {'parts': 1, 'cost': 0.025, 'currency': 'USD', 'encoding': 'GSM-7', 'characters': 22, 'message': 'Notifox: Hello, world!'}
```

## Error Handling

```python
import notifox

client = notifox.NotifoxClient(api_key="your_api_key")

try:
    response = client.send_alert(audience="admin", alert="System is running low on memory")
    print(f"Alert sent! Message ID: {response.get('message_id')}")
except notifox.NotifoxAuthenticationError as e:
    print(f"Authentication failed: {e}")
except notifox.NotifoxValidationError as e:
    print(f"Validation error: {e}")
    if e.error:
        print(f"Error type: {e.error}")
except notifox.NotifoxInsufficientBalanceError:
    print("Insufficient balance. Please add funds to your account.")
except notifox.NotifoxRateLimitError:
    print("Rate limit exceeded. Please wait before sending more alerts.")
except notifox.NotifoxServerError as e:
    print(f"Server error: {e}")
except notifox.NotifoxAPIError as e:
    print(f"API error ({e.status_code}): {e}")
except notifox.NotifoxConnectionError as e:
    print(f"Connection failed: {e}")
```

Available exceptions:
- `NotifoxError` - Base exception for all Notifox errors
- `NotifoxAuthenticationError` - Authentication failed (401/403)
- `NotifoxValidationError` - Request validation failed (400)
- `NotifoxInsufficientBalanceError` - Insufficient balance (402)
- `NotifoxRateLimitError` - Rate limit exceeded (429)
- `NotifoxServerError` - Server errors (500)
- `NotifoxAPIError` - General API errors
- `NotifoxConnectionError` - Network/connection errors