from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException

from starlette.status import HTTP_200_OK  # TODO: swap starlette for fastapi
from starlette.status import HTTP_201_CREATED  # TODO: swap starlette for fastapi
from starlette.status import HTTP_404_NOT_FOUND  # TODO: swap starlette for fastapi

from app.models.cleaning import CleaningCreate
from app.models.cleaning import CleaningPublic
from app.db.repositories.cleanings import CleaningsRepository
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.get('/', response_model=List[CleaningPublic], name='cleanings:get-all-cleanings')
async def get_all_cleanings(
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> List[CleaningPublic]:
    # cleanings = [
    #     {'id': 1, 'name': 'My house', 'cleaning_type': 'full_clean', 'price_per_hour': 29.99},
    #     {'id': 2, 'name': "Someone else's house", 'cleaning_type': 'spot_clean', 'price_per_hour': 19.99},
    # ]
    cleanings = await cleanings_repo.get_all_cleanings()
    return cleanings
    # return [{'id': 1, 'name': 'fake_cleaning', 'price': 0}]


@router.post('/', response_model=CleaningPublic, name='cleanings:create-cleaning', status_code=HTTP_201_CREATED)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)

    return created_cleaning


@router.get('/{id}/', response_model=CleaningPublic, name='cleanings:get-cleaning-by-id')
async def get_cleaning_by_id(
    id: int, cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository))
) -> CleaningPublic:
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id)

    if not cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='No cleaning found with that id.')
    
    return cleaning

