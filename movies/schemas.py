import dataclasses
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel


class MovieIn(BaseModel):
    name: str = None
    plot: str = None
    genres: List[str] = None
    casts: List[str] = None
    test: str = None


class MovieUpdate(MovieIn):
    name: Optional[str]
    plot: Optional[str]
    genres: Optional[List[str]]
    casts: Optional[List[str]]
    test: Optional[str]


class MovieOut(MovieIn):
    id: int
    name: Optional[str]
    plot: Optional[str]
    genres: Optional[List[str]]
    casts: Optional[List[str]]
    test: Optional[str]

    class Config:
        orm_mode = True


@dataclasses.dataclass
class MovieQuery:
    id: Optional[int] = Query(
        None, title="Movie's ID", description="Search movie by identifier"
    )
    name: Optional[str] = Query(
        None, title="Movie's name", description="Search movie by name"
    )
    plot: Optional[str] = Query(
        None, title="Movie's plot", description="Search movie by plot"
    )
    genres: Optional[List[str]] = Query(
        None, title="Movie's genres", description="Search movie by genres list"
    )
    casts: Optional[List[str]] = Query(
        None, title="Movie's casts", description="Search movie by genres list"
    )
    test: Optional[str] = Query(
        None, title="Movie's test", description="Search movie by test"
    )
