from fastapi import HTTPException


class IncomeNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Income not found.")


class AccountBalanceWillGoNegativeException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="After this operation account balance will go negative."
                                                 "Change amount of the operation.")

