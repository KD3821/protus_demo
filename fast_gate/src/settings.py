from pydantic import AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_expiration: int = 300
    jwt_refresh_expiration: int = 600
    api_key: str
    auth_host: str
    auth_port: int
    payments_host: str
    payments_port: int
    amqp_dsn: AmqpDsn
    service_name: str = "gateway"
    redis_url: str
    redis_expiration: int = 60
    log_file: str = "gateway.log"


fast_gate_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
