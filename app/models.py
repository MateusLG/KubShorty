# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base  # Importa a Base

class URL(Base):
    __tablename__ = "urls"  # Nome da tabela no PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    
    # O código curto, ex: "aBcD12".
    codigo_curto = Column(String(10), unique=True, index=True, nullable=False)
    
    url_original = Column(String, nullable=False)
    
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
