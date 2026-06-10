import requests
from services.api_client import handle_response

BASE_URL = "http://127.0.0.1:8000/api"


def add_income(income_data,access_token):

    headers = {'Authorization': 'Bearer ' + access_token}

    response = requests.post(f'{BASE_URL}/incomes', json=income_data, headers=headers)

    return handle_response(response)

def get_income_by_user_id(access_token):

    headers = {'Authorization': 'Bearer ' + access_token}

    response = requests.get(f'{BASE_URL}/incomes', headers=headers)

    return handle_response(response)

def update_income_by_income_id(income_id,access_token,income_data):

    headers = {'Authorization': 'Bearer ' + access_token}

    response = requests.patch(f'{BASE_URL}/incomes/{income_id}', json=income_data, headers=headers)

    return handle_response(response)

def delete_income_by_income_id(income_id,access_token):

    headers = {'Authorization': 'Bearer ' + access_token}

    response = requests.delete(f'{BASE_URL}/incomes/{income_id}', headers=headers)

    return handle_response(response)

