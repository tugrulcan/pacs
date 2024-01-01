from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = Field(default="postgres", env="POSTGRES_DB")
    DB_USER: str = Field(default="postgres", env="POSTGRES_USER")
    DB_PASSWORD: str = Field(default="postgres", env="POSTGRES_PASSWORD")

    DB_HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    DB_PORT: int = Field(default=5432, env="POSTGRES_PORT")

    HEADLESS: bool = Field(default=True, env="HEADLESS")
    ORTHANC_USERNAME: str = Field(default="orthanc", env="ORTHANC_USERNAME")
    ORTHANC_PASSWORD: str = Field(default="orthanc", env="ORTHANC_PASSWORD")

    PACS_PROVIDER_HOST: str = Field(
        default="localhost", env="PACS_PROVIDER_HOST"
    )
    PACS_PROVIDER_PORT: int = Field(default=8042, env="PACS_PROVIDER_PORT")


config = Settings()
