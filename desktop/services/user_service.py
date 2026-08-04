import requests
from services.api_client import handle_response
from config import load_api_base_url


BASE_URL = f"{load_api_base_url()}"

def update_user_profile(updated_user_profile, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.patch(f"{BASE_URL}/api/auth/me", json=updated_user_profile, headers=headers)

    return handle_response(response)