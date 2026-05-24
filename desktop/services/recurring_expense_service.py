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

def get_recurring_expenses_by_expense_id(expense_id,access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{BASE_URL}/recurring-expenses/{expense_id}", headers=headers)

    return response.json()

def update_recurring_expense(expense_id,payload,access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.patch(f"{BASE_URL}/recurring-expenses/{expense_id}", json=payload, headers=headers)

    return response.json()

def delete_recurring_expense(expense_id,access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.delete(f"{BASE_URL}/recurring-expenses/{expense_id}", headers=headers)

    return response.json()
