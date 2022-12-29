from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    debug: bool = False
    env: str = Field(default="dev", env="environment")
    secret_key: str = Field(
        default="5HeE1i8Yu6hMv1RJgnemX32b4VvMxjUgrpZGhB7zImvOknnhkZGKmIwwhHlaQ7KL"
    )

    db_name: str = Field(env="postgres_db")
    db_user: str = Field(env="postgres_user")
    db_password: str = Field(env="postgres_password")
    db_host: str = Field(env="postgres_host")
    db_port: int = Field(env="postgres_port")

    mongodb_dsm: str = Field(env="mongo_uri", default="mongodb://localhost:27017")
    mongo_dbname: str = Field(env="mongo_dbname", default="mastermind_db")
    redis_host: str = Field(env="redis_host", default="localhost")
    redis_port: int = Field(env="redis_port", default=6379)

    use_cache: bool = True
    test_run: bool = False
    algorithm = "HS256"
    access_token_expire_minutes = 30
    ignore_authentication: bool = True


settings = Settings()
