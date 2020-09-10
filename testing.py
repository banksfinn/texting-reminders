# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import config

account_sid = config.account_sid
auth_token = config.auth_token
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_=config.twilio_number,
                     to=config.personal_number
                 )

print(message.sid)
