from typing import List

from databases import Database

from app.db.repositories.base import BaseRepository
from app.db.repositories.offers import OffersRepository

from app.models.cleaning import CleaningInDB
from app.models.user import UserInDB
from app.models.evaluation import EvaluationCreate
from app.models.evaluation import EvaluationUpdate
from app.models.evaluation import EvaluationInDB
from app.models.evaluation import EvaluationAggregate


CREATE_OWNER_EVALUATION_FOR_CLEANER_QUERY = """
    INSERT INTO cleaning_to_cleaner_evaluations (
        cleaning_id,
        cleaner_id,
        no_show,
        headline,
        comment,
        professionalism,
        completeness,
        efficiency,
        overall_rating
    )
    VALUES (
        :cleaning_id,
        :cleaner_id,
        :no_show,
        :headline,
        :comment,
        :professionalism,
        :completeness,
        :efficiency,
        :overall_rating
    )
    RETURNING no_show,
              cleaning_id,
              cleaner_id,
              headline,
              comment,
              professionalism,
              completeness,
              efficiency,
              overall_rating,
              created_at,
              updated_at;
"""


class EvaluationsRepository(BaseRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.offers_repo = OffersRepository(db)

    async def create_evaluation_for_cleaner(
        self, *, evaluation_create: EvaluationCreate, cleaning: CleaningInDB, cleaner: UserInDB
    ) -> EvaluationInDB:
        async with self.db.transaction():
            created_evaluation = await self.db.fetch_one(
                query=CREATE_OWNER_EVALUATION_FOR_CLEANER_QUERY,
                values={**evaluation_create.dict(), 'cleaning_id': cleaning.id, 'cleaner_id': cleaner.id},
            )

            # also mark offer as completed
            await self.offers_repo.mark_offer_completed(cleaning=cleaning, cleaner=cleaner)

            return EvaluationInDB(**created_evaluation)