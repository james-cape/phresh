from typing import Optional

from pydantic import EmailStr
from pydantic import constr
from pydantic import HttpUrl

from app.models.core import DateTimeModelMixin
from app.models.core import IDModelMixin
from app.models.core import CoreModel


class ProfileBase(CoreModel):
    full_name: Optional[str]
    phone_number: Optional[constr(regex='^\d{1,3}-\d{1,3}?-\d{1,4}?$')]
    bio: Optional[str]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):
    '''
    The only field required to create a profile is the users id
    '''
    user_id: int


class ProfileUpdate(ProfileBase):
    '''
    Allow users to update any or no fields, as long as it's not user_id
    '''
    pass


class ProfileInDB(IDModelMixin, DateTimeModelMixin, ProfileBase):
    user_id: int
    username: Optional[str]
    email: Optional[EmailStr]


class ProfilePublic(ProfileInDB):
    pass