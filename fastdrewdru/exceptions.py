from fastapi import HTTPException, status


class HttpException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = None
    headers = None

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )


class CredentialsException(HttpException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}
