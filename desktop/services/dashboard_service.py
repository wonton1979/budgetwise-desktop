import requests

BASE_URL = "http://127.0.0.1:8000/api"


def get_dashboard_data(year,month,access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        f"{BASE_URL}/dashboard/monthly-summary",
        params={"year": year, "month": month},
        headers=headers
    )

    if response.status_code >= 400:
        raise Exception("Failed to load dashboard summary")

    return response.json()
