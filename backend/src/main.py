from decimal import Decimal

import sqlalchemy as sa
from fastapi import FastAPI

import backend.src.auth.router as auth
from backend.src.budget.models import Account, Income
from backend.src.budget.routers import income
from backend.src.config import AccountTypes, Currencies, DEFAULT_API_PREFIX
from backend.src.database import async_session

app = FastAPI()

app.include_router(auth.router, prefix=f'{DEFAULT_API_PREFIX}', tags=['Users'])
app.include_router(income.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Incomes'])


@app.on_event("startup")
async def seed_db():
    async with async_session() as session:
        accounts = await session.execute(sa.select(Account))
        if not accounts.scalars().all():
            print('seeding db..')

            new_account = Account(
                name='test',
                type=AccountTypes.BANK_ACCOUNT,
                balance=Decimal(1.23),
                currency=Currencies.USD
            )

            session.add(new_account)
            await session.commit()

            new_income = Income(
                name='test',
                currency=Currencies.USD,
                amount=Decimal(1.4),
                replenishment_account_id=new_account.id
            )

            session.add(new_income)
            await session.commit()


@app.get("/")
async def hello_world():
    return {'Hello': 'world'}
