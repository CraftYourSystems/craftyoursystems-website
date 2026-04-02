
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from cys_fastapi.core.config import settings

# ── Password hashing ────────────────────────────────────────
# CryptContext manages multiple hashing schemes.
# "bcrypt" is the algorithm. "auto" means: if you change the
# algorithm later, old hashes still verify (it detects the type).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Turns "mypassword123" into "$2b$12$randomsaltXXXXXXXXXXXX..."
    This is what gets saved to the database.
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Returns True if the plain password matches the stored hash.
    This is used at login. It re-hashes the input and compares.
    """
    return pwd_context.verify(plain_password, hashed_password)

# ── JWT functions ────────────────────────────────────────────
def create_access_token(email: str) -> str:
    """
    Builds and signs a JWT token.

    Payload contains:
    - 'sub'  → the subject (who this token is for) = email
    - 'exp'  → expiry time (NOW + 1 hour, in UTC)
    - 'iat'  → issued at (when the token was created)

    jwt.encode() signs it with our SECRET_KEY using HS256.
    Returns a string like: "eyJhbGci..."
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": email,
        "exp": now + timedelta(hours=settings.JWT_EXPIRE_HOURS),
        "iat": now
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str) -> dict:
    """
    Verifies and decodes a JWT token.

    Raises jwt.ExpiredSignatureError if token is older than 1 hour.
    Raises jwt.InvalidTokenError if token was tampered with.

    Returns the payload dict: { "sub": "user@email.com", "exp": ..., "iat": ... }
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
