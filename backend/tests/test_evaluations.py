from typing import List
from typing import Callable

import pytest

from httpx import AsyncClient

from fastapi import FastAPI
from fastapi import status

from app.models.cleaning import CleaningInDB
from app.models.user import UserInDB
from app.models.offer import OfferInDB
from app.models.evaluation import EvaluationCreate
from app.models.evaluation import EvaluationInDB
from app.db.repositories.evaluations import EvaluationsRepository


pytestmark = pytest.mark.asyncio


class TestEvaluationRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(
            app.url_path_for('evaluations:create-evaluation-for-cleaner', cleaning_id=1, username='bradpitt')
        )
        assert res.status_code != status.HTTP_404_NOT_FOUND
        
        res = await client.get(
            app.url_path_for('evaluations:get-evaluation-for-cleaner', cleaning_id=1, username='bradpitt')
        )
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.get(
            app.url_path_for('evaluations:list-evaluations-for-cleaner', username='bradpitt')
        )
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.get(
            app.url_path_for('evaluations:get-stats-for-cleaner', username='bradpitt')
        )
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestCreateEvaluations:
    async def test_owner_can_leave_evaluation_for_cleaner_and_mark_offer_completed(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user3: UserInDB,
        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        evaluation_create = EvaluationCreate(
            no_show=False,
            headline='Excellent job',
            comment=f'''
Really appreciated the hard work and effort they put into this job!
Though the cleaner took their time, I would definitely hire them again for the quality of their work.
            ''',
            professionalism=5,
            completeness=5,
            efficiency=4,
            overall_rating=5,
        )

        authorized_client = create_authorized_client(user=test_user2)
        res = await authorized_client.post(
            app.url_path_for(
                'evaluations:create-evaluation-for-cleaner',
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=test_user3.username,
            ),
            json={'evaluation_create': evaluation_create.dict()},
        )
        assert res.status_code == status.HTTP_201_CREATED
        evaluation = EvaluationInDB(**res.json())
        assert evaluation.no_show == evaluation_create.no_show
        assert evaluation.headline == evaluation_create.headline
        assert evaluation.overall_rating == evaluation_create.overall_rating

        # check that the offer has now been marked as 'completed'
        res = await authorized_client.get(
            app.url_path_for(
                'offers:get-offer-from-user',
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=test_user3.username,
            )
        )
        assert res.status_code == status.HTTP_200_OK
        assert res.json()['status'] == 'completed'

    async def test_non_owner_cant_leave_review(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user4: UserInDB,
        test_user3: UserInDB,
        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        res = await authorized_client.post(
            app.url_path_for(
                'evaluations:create-evaluation-for-cleaner',
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=test_user3.username,
            ),
            json={'evaluation_create': {'overall_rating': 2}},
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    
    async def test_owner_cant_leave_review_for_wrong_user(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user4: UserInDB,
        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user2)
        res = await authorized_client.post(
            app.url_path_for(
                'evaluations:create-evaluation-for-cleaner',
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=test_user4.username,
            ),
            json={'evaluation_create': {'overall_rating': 1}},
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST


    async def test_owner_cant_leave_multiple_reviews(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user3: UserInDB,
        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user2)
        res = await authorized_client.post(
            app.url_path_for(
                'evaluations:create-evaluation-for-cleaner',
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=test_user3.username,
            ),
            json={"evaluation_create": {"overall_rating": 3}},
        )
        assert res.status_code == status.HTTP_201_CREATED
        res = await authorized_client.post(
            app.url_path_for(
                "evaluations:create-evaluation-for-cleaner",
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=test_user3.username,
            ),
            json={"evaluation_create": {"overall_rating": 1}},
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST