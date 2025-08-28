from typing import Optional

from pydantic import BaseModel

from schemas.account import AccountResponse


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: Optional[str] = None


class UserCreateDB(BaseModel):
    email: str
    hashed_password: str
    first_name: str
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdateDB(BaseModel):
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserProfile(BaseModel):
    id: int
    email: str
    full_name: str


class UserProfileWithAccounts(UserProfile):
    accounts: list[AccountResponse]
