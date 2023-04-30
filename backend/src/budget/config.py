from enum import Enum

# Intentionally did not normalize the database for these next enums, since I do not plan to change them in the future.
# If you need to change these values, take care to normalize the database and change the logic in the application


class Currencies(str, Enum):
    """
    Enum type of currencies supported in app.
    """

    def __str__(self):
        return self.value

    USD = 'USD'
    RUB = 'RUB'
    CNY = 'CNY'
    EUR = 'EUR'
    GBP = 'GBP'
    CAD = 'CAD'


class AccountTypes(str, Enum):
    """
    Enum type of account types supported in app.
    """
    def __str__(self):
        return self.value

    WALLET = 'WALLET'
    BANK_ACCOUNT = 'BANK_ACCOUNT'


class IncomeCategories(str, Enum):
    def __str__(self):
        return self.value

    SALARY = "SALARY"
    ODD_JOBS = "ODD_JOBS"
    FROM_INVESTMENTS = "FROM_INVESTMENTS"
    TRANSFERS = "TRANSFERS"
    OTHER = "OTHER"


class SpendingCategories(str, Enum):
    """
    Enum type of spending categories supported in app
    """
    def __str__(self):
        return self.value

    SUPERMARKETS = 'SUPERMARKETS'
    TRANSFERS = 'TRANSFERS'
    FAST_FOOD = 'FAST_FOOD'
    TAXI = 'TAXI'
    ENTERTAINMENT = 'ENTERTAINMENT'
    MISCELLANEOUS = 'MISCELLANEOUS'
    TRANSPORT = 'TRANSPORT'
    SERVICE = 'SERVICE'
    PHARMACIES = 'PHARMACIES'
    BILLS = 'BILLS'
    CLOTHING = 'CLOTHING'
    BEAUTY = 'BEAUTY'
    HOME_IMPROVEMENT = 'HOME_IMPROVEMENT'
    OTHER = 'OTHER'

