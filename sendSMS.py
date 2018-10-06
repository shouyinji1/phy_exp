from twilio.rest import Client
def sendSMS(to_phone):
    account_sid='账户sid'
    auth_token='账户auth'
    client=Client(account_sid,auth_token)
    message= client.messages.create(
        to=to_phone,
        from_="+发送来源手机号",
        body='有实验课可选，请登录查看'
    )
    print(message.sid)
