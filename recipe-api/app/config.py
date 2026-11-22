"""Settings of the project.

We read the database address from an environment variable (or the .env file).
This keeps passwords out of the code.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/recipe_db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
