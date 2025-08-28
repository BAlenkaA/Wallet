import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

ENV_FILE_PATH = os.path.join(BASE_DIR)


class BaseSetting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="allow",
    )


class AppSettings(BaseSetting):
    TITLE: str = "Wallet API"


class DBSettings(BaseSetting):
    POSTGRES_USER: str = "wallet-app"
    POSTGRES_PASSWORD: str = "0f416487-fcaa-4024-b97b-c5d5a6c2bb3e"
    POSTGRES_DB: str = "wallet_db"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "localhost"


class JWTSettings(BaseSetting):
    SECRET_KEY: str = "0d26a88b-48fc-428b-a846-d161ffe3da45"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class WebhookSettings(BaseSetting):
    WEBHOOK_SECRET_KEY: str = "gfdmhghif38yrf9ew0jkf32"


app_settings = AppSettings()
db_settings = DBSettings()
jwt_settings = JWTSettings()
webhook_settings = WebhookSettings()
