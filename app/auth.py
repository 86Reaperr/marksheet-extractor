from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "marksheet-secret-key"
ALGORITHM = "HS256"

security = HTTPBearer()


def create_access_token():
    expire = datetime.utcnow() + timedelta(hours=24)

    payload = {
        "sub": "api-user",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return True

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )