import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(DOTENV)


class Settings(BaseSettings):
    base_url: str
    admin_password: str
    admin_login: str
    email_for_testing: str

    class ConfigDict(SettingsConfigDict):
        env_file_encoding = "utf-8"
        env_file = DOTENV


settings = Settings()
