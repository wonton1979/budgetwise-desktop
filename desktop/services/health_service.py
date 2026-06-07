import requests
from services.api_client import handle_response


BASE_URL = "http://127.0.0.1:8000/api"


def add_health_record(health_record,access_token):

    headers = {"Authorization": "Bearer " + access_token}

    response = requests.post(BASE_URL + "/health",headers=headers,json=health_record)

    return handle_response(response)

def get_health_records(access_token):

    headers = {"Authorization": "Bearer " + access_token}

    response = requests.get(BASE_URL + "/health",headers=headers)

    return handle_response(response)

def update_health_record(health_record_id,health_record,access_token):

    headers = {"Authorization": "Bearer " + access_token}

    response = requests.patch(BASE_URL + f"/health/{health_record_id}",headers=headers,json=health_record)

    return handle_response(response)

def delete_health_record(health_record_id,access_token):

    headers = {"Authorization": "Bearer " + access_token}

    response = requests.delete(BASE_URL + f"/health/{health_record_id}",headers=headers)

    return handle_response(response)

