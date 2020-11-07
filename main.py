import logging

import uvicorn
from fastapi import FastAPI

from fastDrewDru.db import db
from helloworld.views import helloworld
from movies.views import movies

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="drewdru.com",
    description="REST API for drewdru.com",
    version="0.1.0",
)
app.include_router(movies, prefix="/movies", tags=["movies"])
app.include_router(helloworld, prefix="/helloworld", tags=["helloworld"])


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@movies.put("/", tags=["home"])
async def home():
    logger.info("logging from the root logger")
    return {"version": "0.0.1"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
