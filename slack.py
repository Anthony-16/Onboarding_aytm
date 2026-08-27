import os
import requests
from data import name,email,jobTitle,department,username
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('slack_token')

headers={
            "Authorization": "Bearer "+token, 
            "Content-Type": "application/json",
         }

json={
        "channel": "CN2Q3SLR5",
        "text": "Account Creation Successful for "+name+"\n"+jobTitle+"\n"+department+"\n"+username,
    }

r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=json)

print(r.status_code)
print(r.text)

f = open("data.py", "a")

if r.ok:
    f.write("slack_msg_sent = True\n")
else:
    f.write("slack_msg_sent = False\n")

f.close()
