import logging
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response, status

from movies import crud
from movies.schemas import MovieIn, MovieOut, MovieQuery

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[MovieOut])
async def get_movies(query_filter: MovieQuery = Depends(MovieQuery)) -> Response:
    """Get all movies"""
    return await crud.get_movies(query_filter)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MovieOut)
async def add_movie(
    payload: MovieIn = Body(
        None,
        title="Movie data",
        description="New Movie Data",
    )
) -> Response:
    """Add new movie"""
    movie_id = await crud.add_movie(payload)
    return {"id": movie_id, **payload.dict()}


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(
    id: int = Path(None, title="Movie ID", description="Item Identifier"),
    payload: MovieIn = Body(
        None,
        title="Movie data",
        description="New Movie Data",
    ),
) -> Response:
    """Update movie by id"""
    movie = await crud.get_movie(id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    update_data = payload.dict(exclude_unset=True)
    movie_in_db = MovieIn(**movie)
    updated_movie = movie_in_db.copy(update=update_data)
    return await crud.update_movie(id, updated_movie)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    id: int = Path(None, title="Movie ID", description="Item Identifier")
) -> Response:
    """Delete movie by id"""
    movie = await crud.get_movie(id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return await crud.delete_movie(id)
