import requests
import base64
from reportlab.pdfgen import canvas
from ms_token import acquire_token
from data import delivery,tracking,email,password,username

pdf = canvas.Canvas("new_account.pdf")
pdf.setTitle("New Account Login Info")
pdf.drawString(100,750, "New Account Information")
pdf.drawString(100,700, "Username: "+username)
pdf.drawString(100,670, "Password: "+password)
pdf.save()

f = open("new_account.pdf", "rb")
base64_pdf = base64.b64encode(f.read()).decode('utf-8')



if not delivery:
    delivery = "N/A"

if not tracking:
    tracking = "N/A"

token = acquire_token()

if "access_token" in token:
    endpoint = 'https://graph.microsoft.com/v1.0/users/no-reply@aytm.com/sendMail'
    
    
    email_txt = "I have ordered your laptop here is the tracking information "+tracking+". It will arrive on "+delivery+'.\n\nI have created your AYTM email address. Your credentials are attached.\n\nOnce your laptop arrives:\n1. Install Microsoft Authenticator on your phone.\n2. Email bobbijo@aytm.com to let me know your laptop has arrived — I will send you a temporary access pass.\n\nWhen you open your laptop, select "Set up for work or school", then:\n1. Log in with your AYTM email address.\n2. Go to outlook.office.com and set up Outlook.\n3. Download Chrome and set it as your default browser.\n4. Log in to Slack at aytm.slack.com using OctoPortal.\n\nWhen all steps are complete, send me (Bobbijo) a Slack message.'
    
    email_subject = "Aytm Oboarding"

    email_msg = {
    'Message': {
        'Subject': email_subject,

        'Body': {
            'ContentType': 'Text',
            'Content': email_txt
        },

        'ToRecipients': [
            {
                'EmailAddress': {
                    'Address': email
                }
            }
        ],

        'Attachments': [
            {
                '@odata.type': '#microsoft.graph.fileAttachment',
                'name': 'new_account.pdf',
                'contentType': 'application/pdf',
                'contentBytes': base64_pdf
            }
        ]
    },

    'SaveToSentItems': True
}
    r = requests.post(endpoint,headers={'Authorization': 'Bearer ' + token['access_token']},json=email_msg)
    f.close()
    
    f = open("data.py", "a")
    if r.ok:
        f.write('sent_email = True\n')
    else:
        f.write('sent_email = False\n')
    
    print(r.status_code)
    print(r.text)
    f.close()
