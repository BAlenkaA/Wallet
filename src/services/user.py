from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User
from schemas.user import UserUpdate, UserUpdateDB
from security.password import hash_password
from utilities.validators import validate_email_unique


async def user_update(
    current_user: User,
    updated_data: UserUpdate,
    db: AsyncSession,
):
    updated_data_dict = updated_data.model_dump(exclude_unset=True)
    user_email = updated_data_dict.get("email")
    if user_email and user_email != current_user.email:
        is_unique = await validate_email_unique(
            email=updated_data_dict["email"], db=db)
        if not is_unique:
            raise ValueError("Email already exists in the system.")

    password = updated_data_dict.get("password")
    if password:
        updated_data_dict["hashed_password"] = hash_password(
            updated_data_dict.pop("password")
        )

    user_update_db = UserUpdateDB(**updated_data_dict)
    updated_user = await user_crud.update(
        db_obj=current_user, obj_in=user_update_db, session=db
    )

    return updated_user
