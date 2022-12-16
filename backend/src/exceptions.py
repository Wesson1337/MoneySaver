from fastapi import HTTPException


class NoDataForUpdateException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Add at least 1 valid field to update")


class WrongDataForUpdateException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail=f"Wrong data for update this entity")


class CurrencyNotSupportedException(HTTPException):
    def __init__(self, currency: str) -> None:
        super().__init__(status_code=400, detail=f"Currency '{currency}' not supported in app")
