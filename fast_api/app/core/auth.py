from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(subject: str, expires_delta: int = None):
    expire = datetime.now() + timedelta(minutes=(expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": str(subject), "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None
    
def is_token_expired(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.utcfromtimestamp(exp):
            return True
        return False
    except Exception:
        return True
    
def refresh_access_token(token: str, expires_delta: int = None):
    subject = verify_token(token)
    if subject is None or is_token_expired(token):
        return None
    return create_access_token(subject, expires_delta)

