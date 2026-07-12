import requests
from services.api_client import handle_response

BASE_URL = "http://127.0.0.1:8000"

def update_user_profile(updated_user_profile, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.patch(f"{BASE_URL}/api/auth/me", json=updated_user_profile, headers=headers)

    return handle_response(response)