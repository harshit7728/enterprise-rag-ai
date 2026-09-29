from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    app_name:str="Enterprise Rag AI"

    database_url:str
    redis_url:str
    jwt_secret:str
    jwt_algorithm:str="HS256"
    debug:bool = False
    google_api_key:str
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings=Settings()
