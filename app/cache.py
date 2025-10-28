# app/cache.py
import redis
from .config import settings

# Cria um "Pool" de conexões. É mais eficiente do que 
# criar uma nova conexão toda vez.
pool = redis.ConnectionPool(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=0,
    decode_responses=True  # Decodifica respostas de bytes para strings
)

# --- Função de Dependência (para o FastAPI) ---
# Similar ao get_db, isso nos dá uma conexão do pool
# para usar em cada requisição que precisar do cache.
def get_cache():
    r = redis.Redis(connection_pool=pool)
    try:
        yield r
    finally:
        # Com o pool, não precisamos "fechar" a conexão, 
        # ela é devolvida ao pool automaticamente.
        pass
