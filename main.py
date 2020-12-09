import logging
import logging.config
import os
import sys

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration

from fastdrewdru import config
from fastdrewdru.views import router as fastdrewdru_router
from helloworld.views import router as helloworld_router
from movies.views import router as movies_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
settings = config.get_settings()


# region: Initialize logs
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
sentry_logging = LoggingIntegration(
    level=logging.WARNING,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
sentry_sdk.init(
    settings.SENTRY_DNS,
    traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
    integrations=[sentry_logging],
)
# endregion


app = FastAPI(
    title="drewdru.com",
    description="REST API for drewdru.com",
    version=settings.version,
)


# region: Initialize middlewares
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN_WHITELIST,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX_WHITELIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# endregion


# region: Initialize routers
app.include_router(fastdrewdru_router)
app.include_router(movies_router, prefix="/movies", tags=["movies"])
app.include_router(helloworld_router, prefix="/helloworld", tags=["helloworld"])
# endregion
