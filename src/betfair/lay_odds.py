# Given race course, find all current horse odds for the next race

import requests  
import json

# https://identitysso.betfair.com.au/api/login
# parameters (POST)
# username and password

# Header
#Accept: application/json
#X-Application: <AppKey>
#Content-Type: application/x-www-form-urlencoded 

USERNAME = ""
PASSWORD = ""
APP_KEY = ""

LOGIN_URL = "https://identitysso.betfair.com.au/api/login"

def betfair_login():
    header = {
        "Accept": "application/json",
        "X-Application": APP_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    param = f"username={USERNAME}&password={PASSWORD}"
    response = requests.post(LOGIN_URL, data=param, headers=header)
    data = response.json()

    if data.get("status") == "SUCCESS":
        return data.get("token")
    else:
        return None
    

def betfair_request():
    print("ok")

def get_odds():
    print("ok")

