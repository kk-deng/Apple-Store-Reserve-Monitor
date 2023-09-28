# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class UserSettings(BaseSettings):

    DEBUG: bool = False

    # Credentials
    PART_NUMBER: str
    LOCATION_CODE: str
    TELEGRAM_TOKEN: str
    TELEGRAM_CHAT_ID: str

    # USVISA URLs
    BASE_URI: str = "https://www.apple.com/ca"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings_dev = UserSettings()
