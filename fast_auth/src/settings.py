from pydantic import AmqpDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    pg_dsn: PostgresDsn
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_expiration: int = 300
    jwt_refresh_expiration: int = 600
    api_key: str
    payments_host: str
    payments_port: int
    amqp_dsn: AmqpDsn
    service_name: str = "auth"
    log_file: str = "auth.log"
    demo_host: str
    demo_port: int


fast_auth_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
