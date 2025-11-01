from notifox import NotifoxClient

# Option 1: Pass API key directly
client = NotifoxClient(api_key="your_api_key_here")

response = client.send_alert(
    audience="mathis",
    alert="Hello, world!"
)

print(f"Alert sent: {response}")

