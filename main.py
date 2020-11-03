import uvicorn

from fastapi import FastAPI

from fastDrewDru.db import metadata, database, engine
from helloworld.views import helloworld
from movies.views import movies

metadata.create_all(engine)

app = FastAPI(
    title="drewdru.com",
    description="REST API for drewdru.com",
    version="0.1.0",
)
app.include_router(movies, prefix="/movies", tags=["movies"])
app.include_router(helloworld, prefix="/helloworld", tags=["helloworld"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
