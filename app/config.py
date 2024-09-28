from pydantic_settings import BaseSettings

STATIC_FOLDER = "./static"

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


class Settings(BaseSettings):
    pg_dsn: str
    pg_echo: bool

    admin_username: str
    admin_password_hash: str
    jwt_secret: str

    gmail_email: str
    gmail_password: str

    dadata_api_key: str

    telegram_api_key: str
    telegram_chat_id: str

    openai_api_key: str

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

    show_docs: bool = True


settings = Settings()
