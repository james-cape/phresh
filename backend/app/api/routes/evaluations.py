from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body
from fastapi import Path
from fastapi import status

from app.models.evaluation import EvaluationCreate
from app.models.evaluation import EvaluationInDB
from app.models.evaluation import EvaluationPublic
from app.models.evaluation import EvaluationAggregate

from app.models.user import UserInDB
from app.models.cleaning import CleaningInDB

from app.db.repositories.evaluations import EvaluationsRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.users import get_user_by_username_from_path


router = APIRouter()


@router.post(
    '/{cleaning_id}/',
    response_model=EvaluationPublic,
    name='evaluations:create-evaluation-for-cleaner',
    status_code=status.HTTP_201_CREATED,
)
async def create_evaluation_for_cleaner(
    evaluation_create: EvaluationCreate = Body(..., embed=True),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    cleaner: UserInDB = Depends(get_user_by_username_from_path),
    evals_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),
) -> EvaluationPublic:
    return await evals_repo.create_evaluation_for_cleaner(
        evaluation_create=evaluation_create, cleaner=cleaner, cleaning=cleaning
    )


@router.get(
    '/',
    response_model=List[EvaluationPublic],
    name='evaluations:list-evaluations-for-cleaner',
)
async def list_evaluations_for_cleaner() -> List[EvaluationPublic]:
    return None


@router.get(
    '/stats/',
    response_model=EvaluationAggregate, name='evaluations:get-stats-for-cleaner',
)
async def get_status_for_cleaner() -> EvaluationAggregate:
    return None


@router.get(
    '/{cleaning_id}/',
    response_model=EvaluationPublic,
    name='evaluations:get-evaluation-for-cleaner',
)
async def get_evaluation_for_cleaner() -> EvaluationPublic:
    return None