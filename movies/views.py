import logging
from typing import List

from fastapi import APIRouter, Body, Depends, Path, Response, status

from fastdrewdru.utils import Paginator, get_paginator
from movies import crud
from movies.schemas import MovieIn, MovieOut, MovieQuery

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[MovieOut])
async def get_movies(
    query_filter: MovieQuery = Depends(MovieQuery),
    paginator: Paginator = Depends(get_paginator),
) -> Response:
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
    id = await crud.add_movie(payload)
    return {"id": id, **payload.dict(exclude_unset=True)}


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
    await crud.update_movie(id, payload)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    id: int = Path(None, title="Movie ID", description="Item Identifier")
) -> Response:
    """Delete movie by id"""
    await crud.delete_movie(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
