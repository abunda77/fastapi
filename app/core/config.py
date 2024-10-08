from typing import Dict
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

#from functools import lru_cache
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., json_schema_extra={"env": "PROJECT_NAME"})
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})
    SECRET_KEY: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    ALGORITHM: str = Field(..., json_schema_extra={"env": "ALGORITHM"})
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        ..., json_schema_extra={"env": "ACCESS_TOKEN_EXPIRE_MINUTES"}
    )

    MAIL_MAILER: str = Field(..., json_schema_extra={"env": "MAIL_MAILER"})
    MAIL_HOST: str = Field(..., json_schema_extra={"env": "MAIL_HOST"})
    MAIL_PORT: int = Field(..., json_schema_extra={"env": "MAIL_PORT"})
    MAIL_USERNAME: str = Field(..., json_schema_extra={"env": "MAIL_USERNAME"})
    MAIL_PASSWORD: str = Field(..., json_schema_extra={"env": "MAIL_PASSWORD"})
    MAIL_ENCRYPTION: str = Field(..., json_schema_extra={"env": "MAIL_ENCRYPTION"})
    MAIL_FROM_ADDRESS: str = Field(..., json_schema_extra={"env": "MAIL_FROM_ADDRESS"})

   
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(..., json_schema_extra={"env": "RATE_LIMIT_REQUESTS"})
    RATE_LIMIT_PERIOD: str = Field(..., json_schema_extra={"env": "RATE_LIMIT_PERIOD"})

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    HOME_FRONTEND_URL: str = Field(..., json_schema_extra={"env": "HOME_FRONTEND_URL"})
   

settings = Settings()  # Membuat instance Settings secara langsung
PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000