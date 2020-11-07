from typing import List

from fastapi import APIRouter, HTTPException

from movies import crud
from movies.schemas import MovieIn, MovieOut

movies = APIRouter()


@movies.get("/", response_model=List[MovieOut])
async def index():
    return await crud.get_all_movies()


@movies.post("/", status_code=201)
async def add_movie(payload: MovieIn):
    movie_id = await crud.add_movie(payload)
    return {"id": movie_id, **payload.dict()}


@movies.put("/{id}")
async def update_movie(id: int, payload: MovieIn):
    movie = await crud.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)
    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)

    return await crud.update_movie(id, updated_movie)


@movies.delete("/{id}")
async def delete_movie(id: int):
    movie = await crud.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await crud.delete_movie(id)
