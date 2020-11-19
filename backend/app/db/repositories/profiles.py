from app.db.repositories.base import BaseRepository

from app.models.profile import ProfileCreate
from app.models.profile import ProfileUpdate
from app.models.profile import ProfileInDB

CREATE_PROFILE_FOR_USER_QUERY = """
    INSERT INTO profiles (full_name, phone_number, bio, image, user_id)
    VALUES (:full_name, :phone_number, :bio, :image, :user_id)
    RETURNING id, full_name, phone_number, bio, image, user_id, created_at, updated_at;
"""

GET_PROFILE_BY_USER_ID_QUERY = """
    SELECT id, full_name, phone_number, bio, image, user_id, created_at, updated_at
    FROM profiles
    WHERE user_id = :user_id;
"""


class ProfilesRepository(BaseRepository):
    async def create_profile_for_user(self, *, profile_create: ProfileCreate) -> ProfileInDB:
        created_profile = await self.db.fetch_one(query=CREATE_PROFILE_FOR_USER_QUERY, values=profile_create.dict())

        return created_profile

    async def get_profile_by_user_id(self, *, user_id: int) -> ProfileInDB:
        profile_record = await self.db.fetch_one(query=GET_PROFILE_BY_USER_ID_QUERY, values={'user_id': user_id})

        if not profile_record:
            return None

        return ProfileInDB(**profile_record)