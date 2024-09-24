from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = "https://consult-app-5m2kz.ondigitalocean.app/api/v1"

    class ConfigDict(SettingsConfigDict):
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()