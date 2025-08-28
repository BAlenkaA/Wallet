from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares plain_password and hashed_password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt.
    """
    return pwd_context.hash(password)
