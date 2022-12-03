from fastapi import HTTPException


class NoDataForUpdateException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=422, detail="Add at least 1 valid field to update")
