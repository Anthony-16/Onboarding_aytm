from requests.auth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv
from data import name
import sys
import subprocess

load_dotenv()

#load keys from .env file
bambooKey = os.getenv('bambooKey')
url = "https://api.bamboohr.com/api/gateway.php/aytm/v1/employees/directory"
auth = HTTPBasicAuth(bambooKey, 'Api Key')
headers = {'Accept': 'application/json'}

search_employee = name

r = requests.get(url, headers=headers, auth=auth)
data = r.json()
print(r.status_code)

#find the employee and add data to data.py for later use 
def find(user_input):
    f = open("data.py", "a")
    for employee in data['employees']:
        if employee['displayName'] == user_input:
            print(employee['displayName'] + "\n" + employee['workEmail'] + "\n" + employee['jobTitle'] + "\n" + employee['department'] + "\n" + employee['division'])
            f.write("jobTitle = "+'"'+employee['jobTitle']+'"\ndepartment = '+'"'+employee['department']+'"\n')
            return
    
    f.write('JobTitle = "N/A"\ndepartment= "N/A"\n')
    print("User '"+user_input+"' not found in BambooHR database\nContinuing.\n")
    


find(search_employee)



