import logging
import logging.config
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastdrewdru import config

# from fastdrewdru.db import get_db_service
from fastdrewdru.views import router as fastdrewdru_router
from helloworld.views import router as helloworld_router
from middlewares import SentryMiddleware
from movies.views import router as movies_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
settings = config.get_settings()


app = FastAPI(
    title="drewdru.com",
    description="REST API for drewdru.com",
    version=settings.version,
)


# @app.on_event("startup")
# async def startup():
#     db_service = get_db_service()
#     await db_service.db.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     db_service = get_db_service()
#     await db_service.db.disconnect()


# Inittialize middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN_WHITELIST,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX_WHITELIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SentryMiddleware, dns=settings.SENTRY_DNS, traces_sample_rate=1.0)

# Inittialize routers
app.include_router(fastdrewdru_router)
app.include_router(movies_router, prefix="/movies", tags=["movies"])
app.include_router(helloworld_router, prefix="/helloworld", tags=["helloworld"])
