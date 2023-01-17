from fastapi import FastAPI
from fastapi_utils.timing import add_timing_middleware
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator
import backend.src.auth.router as auth
from backend.src.budget.routers import account, income, spending
from backend.src.config import DEFAULT_API_PREFIX, logger, DEBUG

app = FastAPI()

# routers
app.include_router(auth.router, prefix=f'{DEFAULT_API_PREFIX}', tags=['Users'])
app.include_router(income.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Incomes'])
app.include_router(account.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Accounts'])
app.include_router(spending.router, prefix=f'{DEFAULT_API_PREFIX}/budget', tags=['Spendings'])

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
if DEBUG:
    add_timing_middleware(app, record=logger.info, prefix="app", exclude="metrics")


@app.on_event("startup")
async def startup():
    PrometheusFastApiInstrumentator(
        excluded_handlers=["/metrics"]
    ).instrument(app).expose(app)
