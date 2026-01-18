import notifox

client = notifox.NotifoxClient()

# Send an alert via email
response = client.send_alert(
    audience="mathis",
    alert="Your order has been shipped!",
    channel=notifox.Email
)

print(f"Email sent! Message ID: {response.get('message_id')}")
