import requests

from services.api_client import handle_response
from config import load_api_base_url


BASE_URL = f"{load_api_base_url()}/api"

def add_memorable_day(memorable_day_data,access_token):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(f'{BASE_URL}/memorable-day',headers=headers,json=memorable_day_data)

    return handle_response(response)


def get_memorable_days(access_token):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(f'{BASE_URL}/memorable-day',headers=headers)

    return handle_response(response)

def patch_memorable_day(access_token,memorable_day_data,memorable_day_id):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.patch(f'{BASE_URL}/memorable-day/{memorable_day_id}',headers=headers,json=memorable_day_data)

    return handle_response(response)

def delete_memorable_day(access_token,memorable_day_id):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.delete(f'{BASE_URL}/memorable-day/{memorable_day_id}',headers=headers)

    return handle_response(response)

