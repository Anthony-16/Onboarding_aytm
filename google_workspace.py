from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

def run_google_workspace(variables):
    output = ""
    split = variables['name'].split()


    SCOPES = [
        "https://www.googleapis.com/auth/admin.directory.user",
        "https://www.googleapis.com/auth/admin.directory.group.member",
        "https://www.googleapis.com/auth/admin.directory.group"
    ]

    credentials = service_account.Credentials.from_service_account_file(
        "service-account.json",
        scopes=SCOPES,
    )

    #account needs permission to create users and assign groups
    delegated = credentials.with_subject("admin@aytm.com")
    delegated.refresh(Request())
    access_token = delegated.token

    headers = {
        "Authorization": "Bearer "+access_token,
        "Content-Type": "application/json",
    }

    json = {
        "primaryEmail": variables['username'],
        "name": {
            "givenName": split[0],
            "familyName": split[1]
        },
        "password": variables['password']
    }

    r = requests.post("https://admin.googleapis.com/admin/directory/v1/users",headers=headers,json=json)
    output = output + str(r.status_code) + "\n"
    output = output + r.text + "\n"

    if r.ok:
        variables['google_account_created'] = True
    else:
        variables['google_account_created'] = False

    json = {
            "email": variables['username'],
            "role": "MEMBER"
    }

    r = requests.post("https://admin.googleapis.com/admin/directory/v1/groups/01664s550p30o2n/members",headers=headers,json=json)

    output = output + str(r.status_code) + "\n"
    output = output + r.text + "\n"

    if r.ok:
        variables['default_google_group_assigned'] = True
    else:
        variables['default_google_group_assigned'] = False

    return output
