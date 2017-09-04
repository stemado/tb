from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC8d6b9963f18e85624605eb8acf34d5a4"
# Your Auth Token from twilio.com/console
auth_token  = "44ce57127281c87bbffbf2bf5f3ca23f"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+16202247982", 
    from_="+14172834893 ",
    body="Hello from Python!")

print(message.sid)