from fastapi import HTTPException
from starlette import status


class IncomeNotFoundException(HTTPException):
    def __init__(self, income_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Income with id {income_id} is not found"
        )


class AccountNotFoundException(HTTPException):
    def __init__(self, account_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with id {account_id} is not found"
        )


class AccountBalanceWillGoNegativeException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="After this operation account balance will go negative. Change amount of the operation"
        )


class ReplenishmentAccountNotExistsException(HTTPException):
    def __init__(self, replenishment_account_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Replenishment account with id {replenishment_account_id} doesn't exist"
        )


class UserNotExistsException(HTTPException):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} doesn't exist"
        )


class ReplenishmentAccountNotBelongsToUserException(HTTPException):
    def __init__(self, replenishment_account_id: int, user_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account with id {replenishment_account_id} not belongs to user with id {user_id}"
        )