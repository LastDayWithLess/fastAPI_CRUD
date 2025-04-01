from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWD: str
    DB_NAME: str

    @property
    def DATABASE_url_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()