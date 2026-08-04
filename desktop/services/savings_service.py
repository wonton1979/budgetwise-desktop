import requests
from services.api_client import handle_response
from config import load_api_base_url


BASE_URL = f"{load_api_base_url()}"


def get_savings_by_user_id(access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.get(BASE_URL + "/api/savings/",headers=headers)

    return handle_response(response)

def add_new_savings(savings_data,access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.post(BASE_URL + "/api/savings/",headers=headers,json=savings_data)

    return handle_response(response)

def update_savings(savings_id,updated_savings_data,access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.patch(BASE_URL + f"/api/savings/{savings_id}",headers=headers,json=updated_savings_data)

    return handle_response(response)

def delete_savings(savings_id,access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.delete(BASE_URL + f"/api/savings/{savings_id}",headers=headers)

    return handle_response(response)
