import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

def create_token(user_id: str, role: str = "user", expires_in: int = 60) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=expires_in),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def create_agent_token(expires_in: int = 60) -> str:
    return create_token(user_id="macro-agent", role="agent", expires_in=expires_in)

def verify_token(token: str) -> dict:
    """
    Decode and validate a JWT. Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError if invalid.
    Returns the payload as a dict.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise PermissionError("Token has expired")
    except jwt.InvalidTokenError:
        raise PermissionError("Invalid token")
