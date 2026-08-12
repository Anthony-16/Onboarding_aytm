import requests
import time
import sys
from ms_token import acquire_token


token = acquire_token()
endpoint = 'https://graph.microsoft.com/v1.0/users/'
laptop = "windows"
user_id = -1

if "access_token" not in token:
    sys.exit()

auth = {'Authorization': 'Bearer ' + token['access_token']}

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
        r = requests.get(endpoint,headers=auth)
        
        if r.ok and r.json()[key] == value:
            time.sleep(6)
            return True
        else:
            counter += 1
            time.sleep(6)

    return False


def delete_account(user_id):
    r = requests.delete(endpoint+user_id,headers=auth)
    return r.status_code


def create_account():

    #intial account creation
    r = requests.post(endpoint,headers=auth, json=account_params)      
    if r.ok:
        user_id = r.json()['id']
    else:
        return r.status_code

    #add usage location
    if check_update(endpoint+user_id, "id", user_id) == True:
        r = requests.patch(endpoint+user_id,headers=auth, json=additional_info)
    else:
        delete_account(user_id)
        return r.status_code

    #assign licenses
    if check_update(endpoint+user_id+"?$select=usageLocation", "usageLocation", "US") == True:
        r = requests.post(endpoint+user_id+"/assignLicense",headers=auth, json=licenses)
    else:
        delete_account(user_id)
        return r.status_code

    #assign group 
    if r.ok:
        group_url = "https://graph.microsoft.com/v1.0/groups/"
        group = {
            "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/"+user_id
        }
        r = requests.post(group_url+'6c2bfbec-a0ee-4846-b15f-570fce5daa5b/members/$ref',headers=auth, json=group)
    else:
        delete_account(user_id)
        return r.status_code

    #assign os specific group
    if r.ok:
        if laptop == "mac":
            r = requests.post(group_url+'2caa48fe-ed5b-44f1-932e-4c2eac735b4b/members/$ref',headers=auth, json=group)
            if(r.ok):
                return r.status_code
            else:
                delete_account(user_id)
                return r.status_code
        elif laptop == "windows":
            r = requests.post(group_url+'093942c4-d55e-4a00-b35c-753b7df1fbe9/members/$ref',headers=auth, json=group)
            if(r.ok):
                return r.status_code
            else:
                delete_account(user_id)
                return r.status_code
    else:
        delete_account(user_id)
        return r.status_code
    


code = create_account()
print(code)






