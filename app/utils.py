# app/utils.py
import secrets
import string

def gerar_codigo_curto(tamanho: int = 6) -> str:
    """Gera um código aleatório seguro para a URL."""
    # Usa letras (maiúsculas/minúsculas) e dígitos
    caracteres = string.ascii_letters + string.digits
    
    # `secrets` é criptograficamente seguro, o que evita colisões
    return "".join(secrets.choice(caracteres) for _ in range(tamanho))
