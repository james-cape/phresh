from typing import List

from fastapi import HTTPException
from fastapi import status

# from asyncpg.exceptions import UniqueViolationError

from app.db.repositories.base import BaseRepository

from app.models.cleaning import CleaningInDB

from app.models.user import UserInDB

from app.models.offer import OfferCreate
from app.models.offer import OfferUpdate
from app.models.offer import OfferInDB


CREATE_OFFER_FOR_CLEANING_QUERY = """
    INSERT INTO user_offers_for_cleanings (cleaning_id, user_id, status)
    VALUES (:cleaning_id, :user_id, :status)
    RETURNING cleaning_id, user_id, status, created_at, updated_at;
"""

LIST_OFFERS_FOR_CLEANING_QUERY = """
    SELECT cleaning_id, user_id, status, created_at, updated_at
    FROM user_offers_for_cleanings
    WHERE cleaning_id = :cleaning_id;
"""

GET_OFFER_FOR_CLEANING_FROM_USER_QUERY = """
    SELECT cleaning_id, user_id, status, created_at, updated_at
    FROM user_offers_for_cleanings
    WHERE cleaning_id = :cleaning_id and user_id = :user_id;
"""


class OffersRepository(BaseRepository):
    async def create_offer_for_cleaning(self, *, new_offer: OfferCreate) -> OfferInDB:
        created_offer = await self.db.fetch_one(
            query=CREATE_OFFER_FOR_CLEANING_QUERY,
            values={**new_offer.dict(), 'status': 'pending'},
        )
        return OfferInDB(**created_offer)


    async def list_offers_for_cleaning(self, *, cleaning: CleaningInDB) -> List[OfferInDB]:
        offers = await self.db.fetch_all(
            query=LIST_OFFERS_FOR_CLEANING_QUERY,
            values={'cleaning_id': cleaning.id}
        )

        return [OfferInDB(**offer) for offer in offers]


    async def get_offer_for_cleaning_from_user(self, *, cleaning: CleaningInDB, user: UserInDB) -> OfferInDB:
        offer_record = await self.db.fetch_one(
            query=GET_OFFER_FOR_CLEANING_FROM_USER_QUERY,
            values={'cleaning_id': cleaning.id, 'user_id': user.id},
        )

        if not offer_record:
            return None

        return OfferInDB(**offer_record)
    