from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Path
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

# from starlette.status import HTTP_200_OK  # TODO: swap starlette for fastapi
# from starlette.status import HTTP_201_CREATED  # TODO: swap starlette for fastapi
# from starlette.status import HTTP_404_NOT_FOUND  # TODO: swap starlette for fastapi

from app.models.user import UserCreate
from app.models.user import UserUpdate
from app.models.user import UserInDB
from app.models.user import UserPublic

from app.models.cleaning import CleaningCreate
from app.models.cleaning import CleaningUpdate
from app.models.cleaning import CleaningPublic

from app.db.repositories.cleanings import CleaningsRepository

from app.api.dependencies.database import get_repository

from app.api.dependencies.auth import get_current_active_user


router = APIRouter()

# @router.get('/', response_model=List[CleaningPublic], name='cleanings:get-all-cleanings')
# async def get_all_cleanings(
#     cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
# ) -> List[CleaningPublic]:
#     cleanings = await cleanings_repo.get_all_cleanings()
#     return cleanings


@router.post('/', response_model=CleaningPublic, name='cleanings:create-cleaning', status_code=status.HTTP_201_CREATED)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=current_user)

    return created_cleaning


# @router.get('/{id}/', response_model=CleaningPublic, name='cleanings:get-cleaning-by-id')
# async def get_cleaning_by_id(
#     id: int, cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository))
# ) -> CleaningPublic:
#     cleaning = await cleanings_repo.get_cleaning_by_id(id=id)

#     if not cleaning:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='No cleaning found with that id.')
    
#     return cleaning


# @router.put('/{id}/', response_model=CleaningPublic, name='cleanings:update-cleaning-by-id')
# async def update_cleaning_by_id(
#     id: int = Path(..., ge=1, title='The ID of the cleaning to update.'),
#     cleaning_update: CleaningUpdate = Body(..., embed=True),
#     cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
# ) -> CleaningPublic:
#     updated_cleaning = await cleanings_repo.update_cleaning(id=id, cleaning_update=cleaning_update)

#     if not updated_cleaning:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='No cleaning found with that ID.')
    
#     return updated_cleaning


# @router.delete('/{id}', response_model=int, name='cleanings:delete-cleaning-by-id')
# async def delete_cleaning_by_id(
#     id: int = Path(..., ge=1, title='The ID of the cleaning to delete.'),
#     cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
# ) -> int:
#     deleted_id = await cleanings_repo.delete_cleaning_by_id(id=id)

#     if not deleted_id:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='No cleaning found with that id.')
    
#     return deleted_id