import twilio
from twilio.rest import Client

#calling user
def calling_user():
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'your key'
    auth_token = 'your token'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            record = True,
                            url='http://demo.twilio.com/docs/voice.xml',
                            to='+91758xxxx5',
                            from_='+12013808303'
                        )

    print(call.sid)
