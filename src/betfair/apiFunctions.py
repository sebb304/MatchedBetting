import requests  
import json
from datetime import datetime, timezone

USERNAME = ""
PASSWORD = ""
APP_KEY = ""

LOGIN_URL = "https://identitysso.betfair.com.au/api/login"
BETTING_URL = "https://api.betfair.com/exchange/betting/json-rpc/v1"

# Login to betfair and returns token
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
    
# Gets all horse races from current time
def get_markets(token):
    header = {
        "X-Application": APP_KEY,
        "X-Authentication": token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    current_time_str = now.strftime("%H:%M:%S")
    start = f"{today_str}T{current_time_str}Z"
    end   = f"{today_str}T23:59:00Z"

    body = [{
        "jsonrpc": "2.0",
        "method": "SportsAPING/v1.0/listMarketCatalogue",
        "params": {
            "filter": {
                "eventTypeIds": ["7"],
                "marketTypeCodes": ["WIN",],
                "marketCountries": ["AU"],
                "marketStartTime": {"from": start, "to": end}
            },
            "maxResults": "10",
            "marketProjection": [
                "MARKET_START_TIME",
                "RUNNER_METADATA",
                "RUNNER_DESCRIPTION",
                "EVENT"
            ]
        },
        "id": 1
    }]

    response = requests.post(BETTING_URL, headers=header, json=body)
    response.raise_for_status()
    return response.json()[0]["result"][0]

# Gets horse names
def get_runners(tokne, market_id):
    header = {
        "X-Application": APP_KEY,
        "X-Authentication": token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    body = [{
        "jsonrpc": "2.0",
        "method": "SportsAPING/v1.0/listMarketCatalogue",
        "params": {
            "filter": {"marketIds": [market_id]},
            "marketProjection": ["RUNNER_DESCRIPTION"],
            "maxResults": 1
        },
        "id": 1
    }]

    response = requests.post(BETTING_URL, headers=header, json=body)
    response.raise_for_status()
    return response.json()[0]


# Gets back/lay odds of horses in given race
def get_lay_odds(token, market_id):
    header = {
        "X-Application": APP_KEY,
        "X-Authentication": token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    body = [{
        "jsonrpc": "2.0",
        "method": "SportsAPING/v1.0/listMarketBook",
        "params": {
            "marketIds": [market_id],
            "priceProjection": {
                "priceData": ["EX_BEST_OFFERS"],
                "virtualise": False,
                "rolloverStakes": False
            }
        },
        "id": 1
    }]

    response = requests.post(BETTING_URL, headers = header, json=body)
    response.raise_for_status()
    return response.json()[0]["result"][0]
