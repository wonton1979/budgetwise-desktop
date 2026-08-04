import requests
from services.api_client import handle_response

from config import load_api_base_url


BASE_URL = f"{load_api_base_url()}"


def register_user(username, email, password, family_code=""):
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "family_code": family_code or "",
    }

    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)

    return handle_response(response)


def login_user(email, password):
    payload = {
        "username": email,
        "password": password,
    }

    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=payload,
        timeout=5
    )

    return handle_response(response)

def get_current_user_profile(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{BASE_URL}/api/auth/me",headers=headers)

    return handle_response(response)