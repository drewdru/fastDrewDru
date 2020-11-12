from typing import List

from fastapi import APIRouter, HTTPException, Response, status

from movies import crud
from movies.schemas import MovieIn, MovieOut

movies = APIRouter()


@movies.get("/", status_code=status.HTTP_200_OK, response_model=List[MovieOut])
async def index() -> Response:
    return await crud.get_all_movies()


@movies.post("/", status_code=status.HTTP_201_CREATED, response_model=MovieOut)
async def add_movie(payload: MovieIn) -> Response:
    movie_id = await crud.add_movie(payload)
    return {"id": movie_id, **payload.dict()}


@movies.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(id: int, payload: MovieIn) -> Response:
    movie = await crud.get_movie(id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    update_data = payload.dict(exclude_unset=True)
    movie_in_db = MovieIn(**movie)
    updated_movie = movie_in_db.copy(update=update_data)
    return await crud.update_movie(id, updated_movie)


@movies.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(id: int) -> Response:
    movie = await crud.get_movie(id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return await crud.delete_movie(id)
