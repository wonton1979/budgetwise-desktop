class SessionExpiredError(Exception):
    pass

class PermissionDeniedError(Exception):
    pass

class ResourceNotFoundError(Exception):
    pass

class ServerError(Exception):
    pass

class ApiConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class ApiError(Exception):
    pass


def handle_response(response):
    if response.status_code == 401:
        detail = response.json().get("detail", "")

        if detail == "Token expired" or detail == "Token refused":
            raise SessionExpiredError("Session Expired")

        raise AuthenticationError(response.json().get("detail", ""))

    if response.status_code == 403:
        raise PermissionDeniedError("Permission Denied")

    if response.status_code == 404:
        raise ResourceNotFoundError(response.json().get("detail", ""))

    if response.status_code == 409:
        raise ApiError(" You can't add two weight records in a same day.\n\n Please amend the existing one by click the point on chart.")

    if response.status_code >= 500:
        raise ServerError("Server error")

    if response.status_code >= 400:
        detail = response.json().get("detail", "Request failed")
        raise ApiError(detail)

    return response.json()