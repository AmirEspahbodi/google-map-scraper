from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_DEBUG: bool
    HOST: str
    PORT: int
    ENVIRONMENT: str
    WORKER: int
    SEARCH_QUERY_ITEMS_SEPARATOR: str
    PICTURES_DIRECTORY: str
    NOT_IMPORTED_SHEETS_DIRECTORY: str
    IMPORTED_SHEETS_DIRECTORY: str
    PARENT_DIRECTORY_PROJECTS_MAIN_FILE: str
    LISTING_TYPE_ITEMS_SEPARATOR: str
    model_config = SettingsConfigDict(
        env_file="../.env", extra="ignore", env_file_encoding="utf-8"
    )


AppConfig = AppSettings()
