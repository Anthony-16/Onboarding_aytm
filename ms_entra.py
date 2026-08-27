import requests
import time
import sys
import string
import secrets
from ms_token import acquire_token
from data import name,os,location


def create_pass():
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*_-+="
    return ''.join(secrets.choice(alphabet) for i in range(16))


def check_update(endpoint, key, value):
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

    f = open("data.py", "a")

    #intial account creation
    r = requests.post(endpoint,headers=auth, json=account_params)      
    print(r.status_code)
    print(r.text)
    if r.ok:
        user_id = r.json()['id']
        f.write('ms_account_created=True\n')
    else:
        user_id=-1
        f.write('ms_account_created=False\n')


    #add usage location
    if check_update(endpoint+user_id, "id", user_id) == True:
        r = requests.patch(endpoint+user_id,headers=auth, json=additional_info)
        print(r.text)
        print(r.status_code)
        if r.ok:
            f.write('ms_usage_location_assigned=True\n')
        else:
            f.write('ms_usage_location_assigned=False\n')
    else:
        f.write('ms_usage_location_assigned=False\n')

    #assign licenses
    if check_update(endpoint+user_id+"?$select=usageLocation", "usageLocation", "US") == True:
        r = requests.post(endpoint+user_id+"/assignLicense",headers=auth, json=licenses)
        print(r.status_code)
        print(r.text)
        if r.ok:
            f.write('ms_license_assigned=True\n')
        else:
            f.write('ms_license_assigned=False\n')
    else:
        f.write('ms_license_assigned=False\n')

    #assign group 
    group_url = "https://graph.microsoft.com/v1.0/groups/"
    group = {
            "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/"+user_id
    }
    r = requests.post(group_url+'6c2bfbec-a0ee-4846-b15f-570fce5daa5b/members/$ref',headers=auth, json=group)
    print(r.status_code)
    print(r.text)
    
    if r.ok:
        f.write('ms_default_group_assigned=True\n')
    else:
        f.write('ms_default_group_assigned=False\n')


    #assign os specific group
    if os == "Mac":
        r = requests.post(group_url+'2caa48fe-ed5b-44f1-932e-4c2eac735b4b/members/$ref',headers=auth, json=group)
        print(r.status_code)        
        print(r.text)
        if r.ok:
            f.write('ms_os_group_assigned=True\n')
        else:
            f.write('ms_os_group_assigned=False\n')

    elif os == "Windows":
        r = requests.post(group_url+'093942c4-d55e-4a00-b35c-753b7df1fbe9/members/$ref',headers=auth, json=group)
        print(r.status_code)
        print(r.text)
        if r.ok:
            f.write('ms_os_group_assigned=True\n')
        else:
            f.write('ms_os_group_assigned=False\n')
        

    f.close()
    

def find(user_input):
    url = 'https://graph.microsoft.com/v1.0/users/'
    
    while url:
        r = requests.get(url,headers={'Authorization': 'Bearer ' + token['access_token']})
        data = r.json()

        for employee in data['value']:
            if employee['userPrincipalName'] and (employee['userPrincipalName'].strip().lower() == user_input.strip().lower()):
                return True
        url = data.get("@odata.nextLink")
    return False
    



token = acquire_token()
endpoint = 'https://graph.microsoft.com/v1.0/users/'
user_id = -1

if "access_token" not in token:
    sys.exit()

auth = {'Authorization': 'Bearer ' + token['access_token']}

split = name.split()
username = split[0].lower() + "." + split[1][0].lower() + "@aytm.com".strip()
counter = 0

while(find(username) == True):
    counter = counter + 1
    username = split[0].lower() + "." + split[1][0].lower() + str(counter) + "@aytm.com".strip()


f = open("data.py", "a")
f.write('username="'+username+'"\n')


password = create_pass()
f.write('password="'+password+'"\n')

f.close()

account_params = {
        "accountEnabled": True,
        "displayName": name,
        "mailNickname": split[0]+'-'+split[1],
        "userPrincipalName": username,
        "passwordProfile" : {
            "forceChangePasswordNextSignIn": True,
            "password": password
            }
        }
 
additional_info = {
        "usageLocation": location
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

create_account()







