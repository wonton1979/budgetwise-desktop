import requests
from services.api_client import handle_response
from config import load_api_base_url


BASE_URL = f"{load_api_base_url()}/api"

def add_expense(expense_data, access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(
        f"{BASE_URL}/expenses",
        json=expense_data,
        headers=headers
    )

    return handle_response(response)

def get_expenses(access_token,payment_method,shopping_type,category,min_amount,max_amount, start_date=None, end_date=None, sort_by = "expense_date",order="asc",page=1,limit=8):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {}

    if payment_method:
        params["payment_method"] = payment_method

    if shopping_type:
        params["shopping_type"] = shopping_type

    if category:
        params["category"] = category

    if min_amount:
        params["min_amount"] = min_amount

    if max_amount:
        params["max_amount"] = max_amount

    if start_date:
        params["start_date"] = start_date

    if end_date:
        params["end_date"] = end_date

    if sort_by:
        params["sort_by"] = sort_by

    if order:
        params["order"] = order

    if page:
        params["page"] = page

    if limit:
        params["limit"] = limit

    response = requests.get(
        f"{BASE_URL}/expenses",
        headers=headers,
        params=params
    )

    return handle_response(response)


def get_expense_by_id(expense_id,access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        f"{BASE_URL}/expenses/{expense_id}",
        headers=headers,
    )

    return handle_response(response)

def update_expense(expense_id,expense_data,access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.patch(
        f"{BASE_URL}/expenses/{expense_id}",
        headers=headers,
        json=expense_data
    )

    return handle_response(response)

def delete_expense(expense_id,access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(
        f"{BASE_URL}/expenses/{expense_id}",
        headers=headers
    )

    return handle_response(response)