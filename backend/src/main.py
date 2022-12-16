from fastapi import FastAPI

import backend.src.auth.router as auth
from backend.src.budget.routers import income
from backend.src.config import DEFAULT_API_PREFIX

app = FastAPI()

app.include_router(auth.router, prefix=f'{DEFAULT_API_PREFIX}', tags=['Users'])
app.include_router(income.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Incomes'])


@app.get("/")
async def hello_world():
    return {'Hello': 'world'}
