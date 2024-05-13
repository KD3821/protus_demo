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
    api_key: str
    auth_host: str
    auth_port: int
    amqp_dsn: AmqpDsn
    service_name: str = "payments"
    log_file: str = "payments.log"


fast_pay_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
