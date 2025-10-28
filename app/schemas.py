# app/schemas.py
from pydantic import BaseModel, HttpUrl

# Schema para os dados que o usuário ENVIA para criar uma URL
class URLBase(BaseModel):
    url_original: HttpUrl  # Pydantic já valida se é uma URL válida!

# Schema para os dados que a API RETORNA para o usuário
class URLInfo(BaseModel):
    url_original: HttpUrl
    url_encurtada: str  # Ex: "http://localhost:8000/aBcD12"
    codigo_curto: str

    # Permite que o Pydantic leia dados de um modelo SQLAlchemy
    class Config:
        from_attributes = True
