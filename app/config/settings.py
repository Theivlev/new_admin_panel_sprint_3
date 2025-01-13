from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    """Настройки DSN."""

    elasticsearch_dsn: AnyHttpUrl
    postgres_dsn: PostgresDsn
    redis_dsn: RedisDsn
    batch_size: int
    timeout: float

    class Config:
        env_file = '.env'

settings = Settings()