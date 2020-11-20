from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import Body
from fastapi import Path
from fastapi import status

from app.models.offer import OfferCreate
from app.models.offer import OfferUpdate
from app.models.offer import OfferPublic
from app.models.offer import OfferInDB

from app.models.user import UserInDB

from app.models.cleaning import CleaningInDB

from app.db.repositories.offers import OffersRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.offers import (
    check_offer_create_permissions,
    check_offer_get_permissions,
    check_offer_list_permissions,
    check_offer_acceptance_permissions,
    get_offer_for_cleaning_from_user_by_path,
)

router = APIRouter()


@router.post(
    '/',
    response_model=OfferPublic,
    name='offers:create-offer',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_offer_create_permissions)],
)
async def create_offer(
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    current_user: UserInDB = Depends(get_current_active_user),
    offers_repo: OffersRepository = Depends(get_repository(OffersRepository)),
) -> OfferPublic:
    return await offers_repo.create_offer_for_cleaning(
        new_offer=OfferCreate(cleaning_id=cleaning.id, user_id=current_user.id)
    )


@router.post('/', response_model=OfferPublic, name='offers:create-offer', status_code=status.HTTP_201_CREATED)
async def create_offer(offer_create: OfferCreate = Body(..., embed=True)) -> OfferPublic:
    return None


@router.get('/',
    response_model=List[OfferPublic],
    name='offers:list-offers-for-cleaning',
    dependencies=[Depends(check_offer_list_permissions)],
)
async def list_offers_for_cleaning(
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    offers_repo: OffersRepository = Depends(get_repository(OffersRepository)),
) -> OfferPublic:
    return await offers_repo.list_offers_for_cleaning(cleaning=cleaning)


@router.get(
    '/{username}/',
    response_model=OfferPublic,
    name='offers:get-offer-from-user',
    dependencies=[Depends(check_offer_get_permissions)],
)
async def get_offer_from_user(offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path)) -> OfferPublic:
    return offer


@router.put(
    '/{username}/',
    response_model=OfferPublic,
    name='offers:accept-offer-from-user',
    dependencies=[Depends(check_offer_acceptance_permissions)],
)
async def accept_offer(
    offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path),
    offers_repo: OffersRepository = Depends(get_repository(OffersRepository)),
) -> OfferPublic:
    return await offers_repo.accept_offer(offer=offer)


@router.put('/', response_model=OfferPublic, name='offers:cancel-offer-from-user')
async def cancel_offer_from_user() -> OfferPublic:
    return None


@router.delete('/', response_model=int, name='offers:rescind-offer-from-user')
async def rescind_offer_from_user() -> OfferPublic:
    return None