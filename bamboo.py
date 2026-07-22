from requests.auth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bambooKey = os.getenv('bambooKey')
url = "https://api.bamboohr.com/api/gateway.php/aytm/v1/employees/directory"
auth = HTTPBasicAuth(bambooKey, 'Api Key')
headers = {'Accept': 'application/json'}

print("Search employee:")
search_employee = input()

r = requests.get(url, headers=headers, auth=auth)

data = r.json()

def find(user_input):
    for employee in data['employees']:
        if employee['displayName'] == user_input:
            print(employee['displayName'] + "\n" + employee['workEmail'] + "\n" + employee['jobTitle'] + "\n" + employee['department'] + "\n" + employee['division'])
            return
    
    print("User '"+user_input+"' not found")



find(search_employee)



