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

    mongodb_dsm = Field(env="mongo_uri", default="mongodb://localhost:27017")
    mongo_dbname = Field(env="mongo_dbname", default="mastermind_db")


settings = Settings()
