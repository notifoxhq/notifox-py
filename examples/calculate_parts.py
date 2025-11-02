from notifox import NotifoxClient

client = NotifoxClient()

# Calculate the parts of the alert
response = client.calculate_parts(
    alert="Hello, world!"
)

print(response) # {'parts': 1, 'cost': 0.025, 'currency': 'USD', 'encoding': 'GSM-7', 'characters': 22, 'message': 'Notifox: Hello, world!'}

response = client.calculate_parts(
    alert="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
)

print(response) # {'parts': 3, 'cost': 0.075, 'currency': 'USD', 'encoding': 'GSM-7', 'characters': 454, 'message': 'Notifox: Lorem ipsum dolor sit amet, .... est laborum.'}

response = client.calculate_parts(
    alert="This text has an emoji in it: 😊" # the emoji forces UCS-2 encoding
)

print(response) # {'parts': 1, 'cost': 0.025, 'currency': 'USD', 'encoding': 'UCS-2', 'characters': 82, 'message': 'Notifox: This text has an emoji in it: 😊'}