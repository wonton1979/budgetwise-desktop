import requests

BASE_URL = "http://127.0.0.1:8000"

def update_display_name(display_name,access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.patch(f"{BASE_URL}/api/auth/me", json=display_name, headers=headers)

    return response.json()