import notifox

# The client automatically reads NOTIFOX_API_KEY from environment
# or you can pass it directly: notifox.NotifoxClient(api_key="your_key")
client = notifox.NotifoxClient()

# Send an alert via SMS
response = client.send_alert(
    audience="mathis",
    alert="Hello, world!",
    channel=notifox.SMS
)

print(f"Alert sent! Message ID: {response.get('message_id')}")

