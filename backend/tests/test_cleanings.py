import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_404_NOT_FOUND  # TODO: swap starlette for fastapi
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY  # TODO: swap starlette for fastapi
from starlette.status import HTTP_201_CREATED  # TODO: swap starlette for fastapi

from app.models.cleaning import CleaningCreate

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture
def new_cleaning():
    return CleaningCreate(
        name='test cleaning',
        description='test description',
        price=0.00,
        cleaning_type='spot_clean',
    )

class TestCleaningsRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for('cleanings:create-cleaning'), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for('cleanings:create-cleaning'), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateCleaning:
    async def test_valid_input_creates_cleaning(
        self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate
    ) -> None:
        res = await client.post(
            app.url_path_for('cleanings:create-cleaning'), json={'new_cleaning': new_cleaning.dict()}
        )
        assert res.status_code == HTTP_201_CREATED

        created_cleaning = CleaningCreate(**res.json())
        assert created_cleaning == new_cleaning