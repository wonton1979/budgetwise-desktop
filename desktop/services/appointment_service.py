import requests
from services.api_client import handle_response


BASE_URL = "http://127.0.0.1:8000/api"


def add_appointment(appointment_details, access_token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    response = requests.post(BASE_URL+"/appointment", json=appointment_details, headers=headers)

    return handle_response(response)


def get_appointments(access_token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    response = requests.get(BASE_URL+"/appointment", headers=headers)

    return handle_response(response)


def update_appointment(appointment_details,appointment_id, access_token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    response = requests.patch(BASE_URL+f"/appointment/{appointment_id}", json=appointment_details, headers=headers)

    return handle_response(response)

def delete_appointment(appointment_id, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }
    response = requests.delete(BASE_URL+f"/appointment/{appointment_id}", headers=headers)

    return handle_response(response)