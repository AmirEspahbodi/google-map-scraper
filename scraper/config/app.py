from pydantic_settings import BaseSettings, SettingsConfigDict


class _AppSettings(BaseSettings):
    model_config = SettingsConfigDict()


AppConfig = _AppSettings()
