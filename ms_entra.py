import requests
import time
import sys
from ms_token import acquire_token


token = acquire_token()
endpoint = 'https://graph.microsoft.com/v1.0/users/'

if "access_token" not in token:
    sys.exit()

#Searching functionality (implement later)
#r = requests.get(endpoint,headers={'Authorization': 'Bearer ' + token['access_token']})
#data = r.json()
# 
#def find(user_input):
#    for employee in data['value']:
#        if employee['mail'] and (employee['mail'].strip().lower() == user_input.strip().lower()):
#            print("User '"+user_input+"' found")
#            found = True
#            return

def check_update(endpoint, key, value):
    print("\nWait up to 1 minute while user data updates\n")
    counter = 0
    while counter <= 10:
        r = requests.get(endpoint,headers={'Authorization': 'Bearer ' + token['access_token']})
        
        if r.ok and r.json()[key] == value:
            time.sleep(1)
            return True
        else:
            counter += 1
            time.sleep(6)

    return False
    
    
account_params = {
        "accountEnabled": True,
        "displayName": "Test User",
        "mailNickname": "Test-User",
        "userPrincipalName": "Test-User@aytm.com",
        "passwordProfile" : {
            "forceChangePasswordNextSignIn": True,
            "password": "vfGoA8250ga@"
            }
        }
 
additional_info = {
        "usageLocation": "US"
    }
  
licenses = {
        "addLicenses": [
            {
                "disabledPlans": [],
                "skuId": "cbdc14ab-d96c-4c30-b9f4-6ada7cdc1d46"
                },
            ],
        "removeLicenses": []
        }

print("Creaing Account")
r = requests.post(endpoint,headers={'Authorization': 'Bearer ' + token['access_token']}, json=account_params)    
print(r.status_code)
print(r.text) 
user_id = r.json()['id']

if check_update(endpoint+user_id, "id", user_id) == True:
    print("Adding usage location")
    r = requests.patch(endpoint+user_id,headers={'Authorization': 'Bearer ' + token['access_token']}, json=additional_info)
    print(r.status_code)
    print(r.text)

if check_update(endpoint+user_id+"?$select=usageLocation", "usageLocation", "US") == True:
    print("Adding Licenses")
    r = requests.post(endpoint+user_id+"/assignLicense",headers={'Authorization': 'Bearer ' + token['access_token']}, json=licenses)
    print(r.status_code)
    print(r.text)

group = {
  "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/"+user_id
}
laptop = "windows"

r = requests.post('https://graph.microsoft.com/v1.0/groups/6c2bfbec-a0ee-4846-b15f-570fce5daa5b/members/$ref',headers={'Authorization': 'Bearer ' + token['access_token']}, json=group)
print(r.status_code)
print(r.text)

if laptop == "mac":
    r = requests.post('https://graph.microsoft.com/v1.0/groups/2caa48fe-ed5b-44f1-932e-4c2eac735b4b/members/$ref',headers={'Authorization': 'Bearer ' + token['access_token']}, json=group)
    print(r.status_code)
    print(r.text)

elif laptop == "windows":
    r = requests.post('https://graph.microsoft.com/v1.0/groups/093942c4-d55e-4a00-b35c-753b7df1fbe9/members/$ref',headers={'Authorization': 'Bearer ' + token['access_token']}, json=group)
    print(r.status_code)
    print(r.text)




