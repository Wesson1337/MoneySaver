from fastapi import HTTPException
from starlette import status


class NoDataForUpdateException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Add at least 1 valid field to update"
        )


class WrongDataForUpdateException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Wrong data for update this entity"
        )


class CurrencyNotSupportedException(HTTPException):
    def __init__(self, currency: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Currency '{currency}' not supported in app"
        )


class NotSuperUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to do this"
        )
