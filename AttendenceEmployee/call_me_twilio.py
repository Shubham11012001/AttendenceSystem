import twilio
from twilio.rest import Client

#calling user
def calling_user():
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC42105d199d3a0a6cf7459457968fb55d'
    auth_token = '0e4be08660b87383a9af231655a26cb4'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            record = True,
                            url='http://demo.twilio.com/docs/voice.xml',
                            to='+917583073685',
                            from_='+12013808303'
                        )

    print(call.sid)