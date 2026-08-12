from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group.member",
    "https://www.googleapis.com/auth/admin.directory.group"
]

credentials = service_account.Credentials.from_service_account_file(
    "service-account.json",
    scopes=SCOPES,
)

delegated = credentials.with_subject("anthony@aytm.com")

delegated.refresh(Request())

access_token = delegated.token

headers = {
    "Authorization": "Bearer "+access_token,
    "Content-Type": "application/json",
}

json = {
    "primaryEmail": "Test-user@aytm.com",
    "name": {
        "givenName": "New",
        "familyName": "User"
    },
    "password": "TempPassword123!"
}

r = requests.post("https://admin.googleapis.com/admin/directory/v1/users",headers=headers,json=json)

print(r.status_code)
print(r.text)

json = {
        "email": "Test-user@aytm.com",
        "role": "MEMBER"
}

r = requests.post("https://admin.googleapis.com/admin/directory/v1/groups/01664s550p30o2n/members",headers=headers,json=json)

print(r.status_code)
print(r.text)
