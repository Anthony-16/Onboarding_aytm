import requests
from ms_token import acquire_token

token = acquire_token()

if "access_token" in token:
    endpoint = 'https://graph.microsoft.com/v1.0/users/no-reply@aytm.com/sendMail'
    
    toUserEmail = "anthony@aytm.com"
    
    email_txt = "I have ordered your laptop and it will arrive on [DATE].\n\nI have created your AYTM email address. Your credentials are attached.\n\nOnce your laptop arrives:\n1. Install Microsoft Authenticator on your phone.\n2. Email bobbijo@aytm.com to let me know your laptop has arrived — I will send you a temporary access pass.\n\nWhen you open your laptop, select 'Set up for work or school', then:\n1. Log in with your AYTM email address.\n2. Go to outlook.office.com and set up Outlook.\n3. Download Chrome and set it as your default browser.\n4. Log in to Slack at aytm.slack.com using OctoPortal.\n\nWhen all steps are complete, send me a Slack message."
    
    email_subject = "Test"

    email_msg = {'Message': {'Subject': email_subject,
                            'Body': {'ContentType': 'Text', 'Content': email_txt},
                            'ToRecipients': [{'EmailAddress': {'Address': toUserEmail}}]
                            },
                'SaveToSentItems': 'true'}

    r = requests.post(endpoint,headers={'Authorization': 'Bearer ' + token['access_token']},json=email_msg)
    
    if r.ok:
        print('Sent email successfully')
    else:
        print(r.json())
