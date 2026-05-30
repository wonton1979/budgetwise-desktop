import requests

BASE_URL = "http://127.0.0.1:8000"


def get_savings_by_user_id(access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.get(BASE_URL + "/api/savings/",headers=headers)

    return response.json()

def add_new_savings(savings_data,access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.post(BASE_URL + "/api/savings/",headers=headers,json=savings_data)

    return response.json()

def update_savings(savings_id,updated_savings_data,access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.patch(BASE_URL + f"/api/savings/{savings_id}",headers=headers,json=updated_savings_data)

    return response.json()

def delete_savings(savings_id,access_token):

    headers = {
        "Authorization": "Bearer " + access_token
    }

    response = requests.delete(BASE_URL + f"/api/savings/{savings_id}",headers=headers)

    return response.json()
