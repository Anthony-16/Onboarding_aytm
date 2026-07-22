import requests
import msal
from ms_token import acquire_token


token = acquire_token()
print("Search Email:")
search_email = input()
found = False


if "access_token" in token:
    endpoint = 'https://graph.microsoft.com/v1.0/users/'

    r = requests.get(endpoint,headers={'Authorization': 'Bearer ' + token['access_token']})

    data = r.json()


def find(user_input):
    for employee in data['value']:
        if employee['mail'] and (employee['mail'].strip().lower() == user_input.strip().lower()):
            print("User '"+user_input+"' found)
            found = True
            return
    
    print("User '"+user_input+"' not found\nContinue with account creation? (Yes/No)")
    return input()


answer = find(search_email)

if found == False and answer and answer.strip().lower() == 'yes':
    
    #add request post to create account

    print('Account Created');
else:
    print('Terminating')

