import msal
import os
from dotenv import load_dotenv

load_dotenv()

appID = os.getenv('appID')
secret = os.getenv('secret')
tenID = os.getenv('tenID')

def acquire_token():
    url = "https://login.microsoftonline.com/"+tenID
    app = msal.ConfidentialClientApplication(authority = url, client_id = appID, client_credential = secret)
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token
