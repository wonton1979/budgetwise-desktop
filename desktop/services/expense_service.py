import requests

BASE_URL = "http://127.0.0.1:8000"

def add_expense(expense_data, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(
        f"{BASE_URL}/api/expenses",
        json=expense_data,
        headers=headers
    )

    if response.status_code >= 400:
        raise Exception(response.json().get("detail", "Failed to add expense"))

    return response.json()

def get_expenses(access_token, start_date=None, end_date=None):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {}

    if start_date:
        params["start_date"] = start_date

    if end_date:
        params["end_date"] = end_date

    response = requests.get(
        f"{BASE_URL}/expenses",
        headers=headers,
        params=params
    )

    if response.status_code >= 400:
        raise Exception(response.json().get("detail", "Failed to load expenses"))

    return response.json()