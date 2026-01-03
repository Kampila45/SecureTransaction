from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        protected_namespaces=("settings_",),
    )

    database_url: str
    model_path: str = "app/adapters/outbound/ml/models/model.pkl"
    log_level: str = "INFO"

