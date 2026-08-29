from requests.auth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv
import sys
import subprocess

def run_bamboo(variables):
    output = ""
    load_dotenv()

    #load keys from .env file
    bambooKey = os.getenv('bambooKey')
    url = "https://api.bamboohr.com/api/gateway.php/aytm/v1/employees/directory"
    auth = HTTPBasicAuth(bambooKey, 'Api Key')
    headers = {'Accept': 'application/json'}

    r = requests.get(url, headers=headers, auth=auth)
    data = r.json()
    
    output = output + str((r.status_code)) + "\n"
    output = output + find(variables["name"], data, variables) + "\n"
    
    return output
    

def find(user_input, data, variables):
    for employee in data['employees']:
        if employee['displayName'] == user_input:
            variables['jobTitle'] = employee['jobTitle'] 
            variables['department'] = employee['department']
            return (employee['displayName'] + "\n" + employee['workEmail'] + "\n" + employee['jobTitle'] + "\n" + employee['department'] + "\n" + employee['division'])
            
    variables['jobTitle'] = "N/A"
    variables['department'] = "N/A" 
    return ("User '"+user_input+"' not found in BambooHR database\nContinuing.\n")
    





