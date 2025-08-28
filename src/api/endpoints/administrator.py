from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_admin_user
from crud.administrator import admin_crud
from crud.user import user_crud
from databases.database import get_async_session
from models import Administrator
from schemas.user import (UserCreate, UserCreateDB, UserProfile,
                          UserProfileWithAccounts, UserUpdate)
from security.password import hash_password
from services.user import user_update
from utilities.validators import existing_user

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def admin_profile(
    admin_user: Administrator = Depends(get_admin_user),
    db: AsyncSession = Depends(get_async_session),
):
    return await admin_crud.get_admin_profile_by_id(
        db,
        admin_user.id,
    )


@router.get("/users", response_model=list[UserProfile])
async def get_all_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
    _: Administrator = Depends(get_admin_user),
):
    return await user_crud.get_multi(session=db, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=UserProfileWithAccounts)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    _: Administrator = Depends(get_admin_user),
):
    return await user_crud.get_profile_with_accounts(db, user_id)


@router.post(
    "/",
    response_model=UserProfile,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(
    create_data: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    _: Administrator = Depends(get_admin_user),
):
    if await existing_user(create_data.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {create_data.email} already exists",
        )

    hashed_password = hash_password(create_data.password)
    user_db = UserCreateDB(
        email=create_data.email,
        hashed_password=hashed_password,
        first_name=create_data.first_name,
        last_name=create_data.last_name,
    )

    user = await user_crud.create(session=db, create_schema=user_db)
    return user


@router.patch(
    "/{user_id}",
    response_model=UserProfile,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    updated_data: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: Administrator = Depends(get_admin_user),
):
    found_user = await user_crud.get_profile_by_id(db, user_id)
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    try:
        updated_user = await user_update(found_user, updated_data, db)
        return updated_user
    except ValidationError as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ex.errors())
        ) from ex
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex)
        ) from ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        ) from e


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    _: Administrator = Depends(get_admin_user),
):
    found_user = await user_crud.get_profile_by_id(db, user_id)
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return await user_crud.remove(found_user, db)
