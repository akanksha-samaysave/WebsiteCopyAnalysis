from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
    )

    app_name: str = Field(default="Landing Page Intelligence")
    environment: str = Field(default="development")
    debug: bool = Field(default=True)
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
    allowed_hosts: str = Field(default="*")
    database_url: AnyUrl = Field(default="sqlite:///./backend.db")


settings = Settings()
