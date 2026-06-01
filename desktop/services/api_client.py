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

        if detail == "Token expired":
            raise SessionExpiredError("Session Expired")

        raise AuthenticationError("Authentication Failed")

    if response.status_code == 403:
        raise PermissionDeniedError("Permission Denied")

    if response.status_code == 404:
        raise ResourceNotFoundError("Resource Not Found")

    if response.status_code >= 500:
        raise ServerError("Server error")

    if response.status_code >= 400:
        detail = response.json().get("detail", "Request failed")
        raise ApiError(detail)

    return response.json()