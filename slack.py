import os
import requests
from dotenv import load_dotenv

def run_slack(variables):
    load_dotenv()
    token = os.getenv('slack_token')

    headers={
                "Authorization": "Bearer "+token, 
                "Content-Type": "application/json",
            }
    
    json={
            "channel": "CN2Q3SLR5",
            "text": "Account Creation Successful for "+variables['name']+"\n"+variables['jobTitle']+"\n"+variables['department']+"\n"+variables['username'],
        }

    r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=json)

    output = str(r.status_code) + "\n"
    output = output + r.text + "\n"

    if r.ok:
        variables['slack_msg_sent'] = True
    else:
        variables['slack_msg_sent'] = False

    return output
