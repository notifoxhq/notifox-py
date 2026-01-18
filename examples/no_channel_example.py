import notifox

client = notifox.NotifoxClient()

# Send an alert without specifying a channel
# The channel will be left blank in the request
response = client.send_alert(
    audience="mathis",
    alert="System notification"
)

print(f"Alert sent! Message ID: {response.get('message_id')}")
