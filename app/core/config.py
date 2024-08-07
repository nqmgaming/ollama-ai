from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "My Project"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "nqmgaming"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        case_sensitive = True


settings = Settings()
