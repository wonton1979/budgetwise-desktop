import requests

BASE_URL = "http://127.0.0.1:8000"


def register_user(username, email, password, family_code=""):
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "family_code": family_code or "",
    }

    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)

    if response.status_code >= 400:
        raise Exception(response.json().get("detail", "Registration failed"))

    return response.json()


def login_user(email, password):
    payload = {
        "email": email,
        "password": password,
    }

    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)

    if response.status_code >= 400:
        raise Exception(response.json().get("detail", "Login failed"))

    return response.json()