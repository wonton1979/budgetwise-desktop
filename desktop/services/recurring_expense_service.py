import requests
from services.api_client import handle_response
from config import load_api_base_url


BASE_URL = f"{load_api_base_url()}/api"

def add_recurring_expense(payload,access_token):

   headers = {
        "Authorization": f"Bearer {access_token}"
    }

   response = requests.post(f"{BASE_URL}/recurring-expenses", json=payload, headers=headers)

   return handle_response(response)

def get_recurring_expense(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{BASE_URL}/recurring-expenses", headers=headers)

    return handle_response(response)

def get_recurring_expenses_by_expense_id(expense_id,access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{BASE_URL}/recurring-expenses/{expense_id}", headers=headers)

    return handle_response(response)

def update_recurring_expense(expense_id,payload,access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.patch(f"{BASE_URL}/recurring-expenses/{expense_id}", json=payload, headers=headers)

    return handle_response(response)

def delete_recurring_expense(expense_id,access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.delete(f"{BASE_URL}/recurring-expenses/{expense_id}", headers=headers)

    return handle_response(response)
