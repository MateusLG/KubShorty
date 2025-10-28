# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings  # Importa as configurações

# 1. Cria o "Engine": o ponto de entrada principal para o DB
engine = create_engine(settings.DATABASE_URL)

# 2. Cria uma fábrica de "Sessões": cada sessão é uma conversa com o DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Cria uma classe "Base" da qual nossos modelos de tabela irão herdar
Base = declarative_base()

# --- Função de Dependência (para o FastAPI) ---
# Isso é um "injetor de dependência" do FastAPI.
# Ele garante que abra uma sessão com o DB quando a requisição 
# começa e a fecha quando ela termina.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
