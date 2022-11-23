from fastapi import HTTPException


class IncomeNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Income not found")



