from datetime import timedelta

from pydantic_settings import BaseSettings


STATIC_FOLDER = "./static"


class Settings(BaseSettings):
    pg_dsn: str
    pg_echo: bool

    admin_username: str
    admin_password_hash: str
    jwt_secret: str

    # s3_endpoint: str
    # s3_cdn_endpoint: str
    # s3_secret_key: str
    # s3_access_key: str
    # s3_region: str

    # redis_username: str
    # redis_password: str
    # redis_host: str
    # redis_port: int
    # redis_db: int

    log_lvl: str = "INFO"


settings = Settings()
