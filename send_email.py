import requests
import base64
from reportlab.pdfgen import canvas
from ms_token import acquire_token

def run_send_email(variables):
    #create the pdf with accout credentials
    pdf = canvas.Canvas("new_account.pdf")
    pdf.setTitle("New Account Login Info")
    pdf.drawString(100,750, "New Account Information")
    pdf.drawString(100,700, "Username: "+variables['username'])
    pdf.drawString(100,670, "Password: "+variables['password'])
    pdf.save()

    f = open("new_account.pdf", "rb")
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    token = acquire_token()

    if "access_token" in token:
        endpoint = 'https://graph.microsoft.com/v1.0/users/no-reply@aytm.com/sendMail'
    
    
        email_txt = "I have ordered your laptop here is the tracking information "+variables['tracking']+". It will arrive on "+variables['delivery']+'.\n\nI have created your AYTM email address. Your credentials are attached.\n\nOnce your laptop arrives:\n1. Install Microsoft Authenticator on your phone.\n2. Email bobbijo@aytm.com to let me know your laptop has arrived — I will send you a temporary access pass.\n\nWhen you open your laptop, select "Set up for work or school", then:\n1. Log in with your AYTM email address.\n2. Go to outlook.office.com and set up Outlook.\n3. Download Chrome and set it as your default browser.\n4. Log in to Slack at aytm.slack.com using OctoPortal.\n\nWhen all steps are complete, send me (Bobbijo) a Slack message.'
    
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
                        'Address': variables['email']
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
    
        if r.ok:
            variables['sent_email'] = True
        else:
            variables['sent_email'] = False
    
        output = str(r.status_code) + "\n"
        output = output + r.text + "\n"
        return output
