from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator
import backend.src.auth.router as auth
from backend.src.budget.routers import account, income, spending
from backend.src.config import DEFAULT_API_PREFIX

app = FastAPI()

app.include_router(auth.router, prefix=f'{DEFAULT_API_PREFIX}', tags=['Users'])
app.include_router(income.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Incomes'])
app.include_router(account.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Accounts'])
app.include_router(spending.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Spendings'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

PrometheusFastApiInstrumentator(
    excluded_handlers=["/metrics"]
).instrument(app).expose(app)
