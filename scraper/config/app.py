from pydantic_settings import BaseSettings, SettingsConfigDict


class _AppSettings(BaseSettings):
    SEARCH_QUERY_ITEMS_SEPARATOR: str
    PICTURES_DIRECTORY: str
    NOT_IMPORTED_SHEETS_DIRECTORY: str
    IMPORTED_SHEETS_DIRECTORY: str
    PARENT_DIRECTORY_PROJECTS_MAIN_FILE: str
    LISTING_TYPE_ITEMS_SEPARATOR: str
    model_config = SettingsConfigDict(
        env_file="../.env", extra="ignore", env_file_encoding="utf-8"
    )


AppConfig = _AppSettings()
