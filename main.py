import logging

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request

from fastDrewDru.config import get_settings
from fastDrewDru.db import db
from helloworld.views import helloworld
from movies.views import movies

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
settings = get_settings()

sentry_sdk.init(settings.SENTRY_DNS, traces_sample_rate=1.0)

app = FastAPI(
    title="drewdru.com",
    description="REST API for drewdru.com",
    version="0.1.0",
)
app.include_router(movies, prefix="/movies", tags=["movies"])
app.include_router(helloworld, prefix="/helloworld", tags=["helloworld"])


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("request", request)
            user_id = "database_user_id"  # when available
            scope.user = {"ip_address": request.client.host, "id": user_id}
            sentry_sdk.capture_exception(e)
        raise e


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.put("/", tags=["home"])
async def home():
    logger.info("logging from the root logger")
    return {"version": "0.0.1"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
