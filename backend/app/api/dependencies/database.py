from typing import Callable
from typing import Type
from databases import Database

from fastapi import Depends
from starlette.requests import Request  # TODO: replace starlette with fastapi

from app.db.repositories.base import BaseRepository


def get_database(request: Request) -> Database:
    return request.app.state._db


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return Repo_type(db)

    return get_repo