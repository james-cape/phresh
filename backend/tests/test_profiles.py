import pytest

from databases import Database

from fastapi import FastAPI
from fastapi import status

from httpx import AsyncClient

from app.models.user import UserInDB

pytestmark = pytest.mark.asyncio


class TestProfilesRoutes:
    '''
    Ensure that no api route returns a 404
    '''
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient, test_user: UserInDB) -> None:
        # Get profile by username
        res = await client.get(app.url_path_for('profiles:get-profile-by-username', username=test_user.username))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        # Update own profile
        res = await client.put(app.url_path_for('profiles:update-own-profile'), json={'profile_update': {}})
        assert res.status_code != status.HTTP_404_NOT_FOUND