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