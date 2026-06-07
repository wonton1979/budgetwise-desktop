import requests
from services.api_client import handle_response ,ApiConnectionError

BASE_URL = "http://127.0.0.1:8000"


def register_user(username, email, password, family_code=""):
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "family_code": family_code or "",
    }

    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)

    return response.json()


def login_user(email, password):
    payload = {
        "username": email,
        "password": password,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=payload,
            timeout=5
        )

    except requests.RequestException:
        raise ApiConnectionError(
            "Cannot connect to server"
        )

    return handle_response(response)

def get_current_user_profile(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"{BASE_URL}/api/auth/me",headers=headers)



    return response.json()