# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import redis
from . import models, schemas, utils, cache, database
from .database import engine, get_db
from .cache import get_cache

# Cria a tabela no DB (se ela não existir)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kube-Shorty")

# --- Endpoint de Criação (POST) ---
@app.post("/encurtar", response_model=schemas.URLInfo)
def encurtar_url(
    request: Request,
    url_data: schemas.URLBase, 
    db: Session = Depends(get_db)):

    """Cria e salva uma nova URL encurtada."""
    codigo = utils.gerar_codigo_curto()
    
    # 2. Cria o objeto do modelo SQLAlchemy
    db_url = models.URL(
        url_original=str(url_data.url_original),  # Converte HttpUrl para string
        codigo_curto=codigo)
    
    # 3. Salva no banco de dados
    db.add(db_url)
    db.commit()
    db.refresh(db_url)  # Pega o ID e data_criacao gerados pelo DB
    
    # 4. Monta a URL de resposta
    url_encurtada_completa = f"{request.base_url}{codigo}"
    
    # 5. Retorna os dados no formato do schema de resposta
    return schemas.URLInfo(
        url_original=db_url.url_original,
        url_encurtada=url_encurtada_completa,
        codigo_curto=db_url.codigo_curto
    )


# --- Endpoint de Redirecionamento (GET) ---
@app.get("/{codigo_curto}")
def redirecionar_url(
    codigo_curto: str, 
    db: Session = Depends(get_db), 
    r: redis.Redis = Depends(get_cache)
):
    """Busca uma URL pelo código e redireciona o usuário."""
    
    # 1. Tenta buscar no CACHE (Redis) primeiro
    url_original = r.get(codigo_curto)
    
    if url_original:
        # Cache HIT! Retorna imediatamente.
        print(f"Cache HIT para: {codigo_curto}")
        return RedirectResponse(url=url_original)
    
    # 2. Cache MISS. Busca no BANCO DE DADOS (PostgreSQL)
    print(f"Cache MISS para: {codigo_curto}. Buscando no DB...")
    db_url = db.query(models.URL).filter(models.URL.codigo_curto == codigo_curto).first()
    
    if db_url is None:
        # Se não achou nem no cache nem no DB, não existe.
        raise HTTPException(status_code=404, detail="URL não encontrada")
        
    #    Define um tempo de expiração (ex: 1 hora)
    r.set(db_url.codigo_curto, db_url.url_original, ex=3600)
    
    # 4. Redireciona o usuário
    return RedirectResponse(url=db_url.url_original)
