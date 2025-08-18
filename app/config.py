import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    DB_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SECRET_KEY: str
    ALGORITHM: str
    KEYCLOAK_BASE_URL: str
    BASE_URL: str
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str

    @property
    def token_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/token"

    @property
    def auth_url(self) -> str:
        return (f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/auth"

        )
    @property
    def logout_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/logout"

    @property
    def userinfo_orl(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/userinfo"

    @property
    def redirect_uri(self) -> str:
        return f"{self.BASE_URL}/api/login/callback"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )
def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


settings = Settings()
database_url = settings.DB_URL

print("DB URL =>", settings.DB_URL)
