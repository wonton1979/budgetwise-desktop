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