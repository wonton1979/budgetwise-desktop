import requests
from services.api_client import handle_response

BASE_URL = "http://127.0.0.1:8000/api"


def get_dashboard_data(year,month,access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        f"{BASE_URL}/dashboard/monthly-summary",
        params={"year": year, "month": month},
        headers=headers
    )

    return handle_response(response)

def get_monthly_spending_chart_data(year, month, access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        f"{BASE_URL}/dashboard/weekly-spending-trend",
        params={"year": year, "month": month},
        headers=headers
    )

    return handle_response(response)

def get_monthly_category_expenses_chart_data(year,month,access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        f"{BASE_URL}/dashboard/category-breakdown",
        params={"year": year, "month": month},
        headers=headers
    )

    return handle_response(response)
