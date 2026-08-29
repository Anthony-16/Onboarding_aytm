import requests
import time
import sys
import string
import secrets
from ms_token import acquire_token

def create_pass():
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*_-+="
    return ''.join(secrets.choice(alphabet) for i in range(16))

def check_update(endpoint, key, value, auth):
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

def create_account(endpoint, auth, account_params, additional_info, licenses, variables):
    output = ""

    #intial account creation
    r = requests.post(endpoint,headers=auth, json=account_params)      
    output = output + str(r.status_code) + "\n"
    output = output + r.text + "\n"
    if r.ok:
        user_id = r.json()['id']
        variables['ms_account_created'] = True
    else:
        user_id=-1
        variables['ms_account_created'] = False


    #add usage location
    if check_update(endpoint+str(user_id), "id", user_id, auth) == True:
        r = requests.patch(endpoint+user_id,headers=auth, json=additional_info)
        output = output + str(r.status_code) + "\n"
        output = output + r.text + "\n"
        if r.ok:
            variables['ms_usage_location_assigned'] = True
        else:
            variables['ms_usage_location_assigned'] = False
    else:
        variables['ms_usage_location_assigned'] = False

    #assign licenses
    if check_update(endpoint+str(user_id)+"?$select=usageLocation", "usageLocation", "US", auth) == True:
        r = requests.post(endpoint+user_id+"/assignLicense",headers=auth, json=licenses)
        output = output + str(r.status_code) + "\n"
        output = output + r.text + "\n"
        if r.ok:
            variables['ms_license_assigned'] = True
        else:
            variables['ms_license_assigned'] = False
    else:
        variables['ms_license_assigned'] = False

    #assign group 
    group_url = "https://graph.microsoft.com/v1.0/groups/"
    group = {
            "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/"+user_id
    }
    r = requests.post(group_url+'6c2bfbec-a0ee-4846-b15f-570fce5daa5b/members/$ref',headers=auth, json=group)
    output = output + str(r.status_code) + "\n"
    output = output + r.text + "\n"
    
    if r.ok:
        variables['ms_default_group_assigned'] = True
    else:
        variables['ms_default_group_assigned'] = False


    #assign os specific group
    if variables['os'] == "Mac":
        r = requests.post(group_url+'2caa48fe-ed5b-44f1-932e-4c2eac735b4b/members/$ref',headers=auth, json=group)
        output = output + str(r.status_code) + "\n"        
        output = output + r.text + "\n"
        if r.ok:
            variables['ms_os_group_assigned'] = True
        else:
            variables['ms_os_group_assigned'] = False

    elif variables['os'] == "Windows":
        r = requests.post(group_url+'093942c4-d55e-4a00-b35c-753b7df1fbe9/members/$ref',headers=auth, json=group)
        output = output + str(r.status_code) + "\n"
        output = output + r.text + "\n"
        if r.ok:
            variables['ms_os_group_assigned'] = True
        else:
            variables['ms_os_group_assigned'] = False
        
    return output
    

def find(user_input, auth):
    url = 'https://graph.microsoft.com/v1.0/users/'
    
    while url:
        r = requests.get(url,headers=auth)
        data = r.json()

        for employee in data['value']:
            if employee['userPrincipalName'] and (employee['userPrincipalName'].strip().lower() == user_input.strip().lower()):
                return True
        url = data.get("@odata.nextLink")
    return False
    
def run_ms_entra(variables):

    token = acquire_token()
    endpoint = 'https://graph.microsoft.com/v1.0/users/'
    user_id = -1

    if "access_token" not in token:
        sys.exit()

    auth = {'Authorization': 'Bearer ' + token['access_token']}

    split = variables['name'].split()
    username = split[0].lower() + "." + split[1][0].lower() + "@aytm.com".strip()
    counter = 0

    while(find(username, auth) == True):
        counter = counter + 1
        username = split[0].lower() + "." + split[1][0].lower() + str(counter) + "@aytm.com".strip()

    variables['username'] = username
    variables['password'] = create_pass()

    account_params = {
            "accountEnabled": True,
            "displayName": variables['name'],
            "mailNickname": split[0]+'-'+split[1],
            "userPrincipalName": variables['username'],
            "passwordProfile" : {
                "forceChangePasswordNextSignIn": True,
                "password": variables['password']
                }
            }
 
    additional_info = {
            "usageLocation": variables['location']
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
    
    out = create_account(endpoint, auth, account_params, additional_info, licenses, variables)
    return out







