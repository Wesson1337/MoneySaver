import aioredis
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi_utils.timing import add_timing_middleware
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

import backend.src.auth.router as auth
from backend.src import config
from backend.src.budget.routers import account, income, spending
from backend.src.config import DEFAULT_API_PREFIX, logger
from backend.src.database import async_session
from backend.src.redis import seed_redis_from_db
import sentry_sdk

sentry_sdk.init(
    dsn=config.SENTRY_SDK_DSN,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

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
add_timing_middleware(app, record=logger.info, prefix="app", exclude="metrics")


# tasks and events
@app.on_event("startup")
async def prometheus_instrumentator():
    Instrumentator(
        excluded_handlers=["/metrics"]
    ).instrument(app).expose(app)


@app.on_event("startup")
@repeat_every(seconds=60 * 60)
async def refresh_redis():
    redis = aioredis.from_url(config.REDIS_URL, password=config.REDIS_PASSWORD, decode_responses=True)
    async with async_session() as session:
        await seed_redis_from_db(session, redis)
    await redis.close()
