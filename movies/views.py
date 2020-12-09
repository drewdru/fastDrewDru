import logging
from typing import List

from fastapi import APIRouter, Body, Depends, Response, status

from movies import crud
from movies.models.movies import MoviesModel
from movies.schemas import MovieIn, MovieOut

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[MovieOut])
async def get_movies(
    movies: MoviesModel = Depends(crud.get_movies),
) -> Response:
    """Get all movies"""
    return movies


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MovieOut)
async def add_movie(
    payload: MovieIn = Body(
        None,
        title="Movie data",
        description="New Movie Data",
    ),
    movie_id: int = Depends(crud.add_movie),
) -> Response:
    """Add new movie"""
    return {"id": movie_id, **payload.dict(exclude_unset=True)}


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(result=Depends(crud.update_movie)) -> Response:
    """Update movie by id"""
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(result=Depends(crud.delete_movie)) -> Response:
    """Delete movie by id"""
    return Response(status_code=status.HTTP_204_NO_CONTENT)
