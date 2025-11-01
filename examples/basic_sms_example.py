from notifox import NotifoxClient

# The client automatically reads NOTIFOX_API_KEY from environment
# or you can pass it directly: NotifoxClient(api_key="your_key")
client = NotifoxClient()

# Send an alert
response = client.send_alert(
    audience="mathis",
    alert="Hello, world!"
)

print(f"Alert sent: {response}")

