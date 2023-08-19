"""
The HyperText Transfer Protocol (HTTP) 401 Unauthorized response status code indicates that the client
request has not been completed because it lacks valid authentication credentials for the requested resource.
"""

import fastapi

from src.utilities.messages.exceptions.http.exc_details import http_401_unauthorized_details


def http_exc_401(detail: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )
