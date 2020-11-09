import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastDrewDru.config import get_settings
from fastDrewDru.db import db
from helloworld.views import helloworld
from middlewares import SentryMiddleware
from movies.views import movies

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title="drewdru.com",
    description="REST API for drewdru.com",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SentryMiddleware, dns=settings.SENTRY_DNS, traces_sample_rate=1.0)

app.include_router(movies, prefix="/movies", tags=["movies"])
app.include_router(helloworld, prefix="/helloworld", tags=["helloworld"])


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/", tags=["home"])
async def home():
    logger.info("logging from the root logger")
    return {"version": "0.0.1"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
