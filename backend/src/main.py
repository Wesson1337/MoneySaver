from fastapi import FastAPI
from budget.routers.income import router as incomes_router

app = FastAPI()

app.include_router(incomes_router, prefix='/api/budget/incomes')


@app.get("/")
async def hello_world():
    return {'Hello': 'world'}
