from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from fastapi import Body

from starlette.status import HTTP_201_CREATED  # TODO: swap starlette for fastapi
from starlette.status import HTTP_404_NOT_FOUND  # TODO: swap starlette for fastapi

from app.api.dependencies.database import get_repository

from app.models.user import UserCreate
from app.models.user import UserPublic

from app.db.repositories.users import UsersRepository

router = APIRouter()

@router.post('/', response_model=UserPublic, name='users:register-new-user', status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    created_user = await user_repo.register_new_user(new_user=new_user)

    return created_user