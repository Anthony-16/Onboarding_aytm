from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
from data import username,name,password

split = name.split()


SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group.member",
    "https://www.googleapis.com/auth/admin.directory.group"
]

credentials = service_account.Credentials.from_service_account_file(
    "service-account.json",
    scopes=SCOPES,
)

delegated = credentials.with_subject("admin@aytm.com")

delegated.refresh(Request())

access_token = delegated.token

headers = {
    "Authorization": "Bearer "+access_token,
    "Content-Type": "application/json",
}

json = {
    "primaryEmail": username,
    "name": {
        "givenName": split[0],
        "familyName": split[1]
    },
    "password": password
}

r = requests.post("https://admin.googleapis.com/admin/directory/v1/users",headers=headers,json=json)
print(r.status_code)
print(r.text)

f = open("data.py", "a")

if r.ok:
    f.write("google_account_created = True\n")
else:
    f.write("google_account_created = False\n")

json = {
        "email": username,
        "role": "MEMBER"
}

r = requests.post("https://admin.googleapis.com/admin/directory/v1/groups/01664s550p30o2n/members",headers=headers,json=json)

print(r.status_code)
print(r.text)

if r.ok:
    f.write("default_google_group_assigned = True\n")
else:
    f.write("default_google_group_assigned = False\n")

f.close()
