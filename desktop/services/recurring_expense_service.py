import requests

BASE_URL = "http://127.0.0.1:8000/api"

def add_recurring_expense(payload,access_token):

   headers = {
        "Authorization": f"Bearer {access_token}"
    }

   response = requests.post(f"{BASE_URL}/recurring-expenses", json=payload, headers=headers)

   return response.json()

def get_recurring_expense(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{BASE_URL}/recurring-expenses", headers=headers)

    return response.json()

