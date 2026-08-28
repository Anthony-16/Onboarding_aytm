import msal
import os
from dotenv import load_dotenv

def acquire_token():
    load_dotenv()

    appID = os.getenv('appID')
    secret = os.getenv('secret')
    tenID = os.getenv('tenID')

    url = "https://login.microsoftonline.com/"+tenID
    app = msal.ConfidentialClientApplication(authority = url, client_id = appID, client_credential = secret)
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token
