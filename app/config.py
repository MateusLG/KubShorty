# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configurações do Banco de Dados (PostgreSQL)
    DATABASE_URL: str

    # Configurações do Cache (Redis)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Carrega as variáveis de um arquivo .env
    model_config = SettingsConfigDict(env_file=".env")

# Cria uma instância única que será usada em todo o app
settings = Settings()
