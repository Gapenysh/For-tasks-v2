from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel


class DBSettings(BaseModel):
    url: str = f"mysql+mysqldb://{username}:{password}@{hostname}/{databasename}"
    echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DBSettings = DBSettings()

    # db_echo: bool = False


settings = Settings()
