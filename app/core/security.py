"""
Authentication and security utilities.

Includes:
- Password hashing with bcrypt (via passlib)
- JWT token generation and validation
- Dependency injection for current user
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: Plain text password.
        
    Returns:
        Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify.
        hashed_password: Previously hashed password.
        
    Returns:
        True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str  # Subject (user ID)
    exp: datetime  # Expiration
    iat: datetime  # Issued at
    scopes: list[str] = []  # Roles/scopes


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    scopes: Optional[list[str]] = None,
) -> str:
    """Create a JWT access token.
    
    Args:
        subject: User ID (subject claim).
        expires_delta: Optional custom expiry. Defaults to settings.access_token_expire_minutes.
        scopes: List of roles/scopes for RBAC.
        
    Returns:
        Encoded JWT token.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    now = datetime.utcnow()
    expire = now + expires_delta

    payload = TokenPayload(
        sub=subject,
        iat=now,
        exp=expire,
        scopes=scopes or [],
    )

    encoded_jwt = jwt.encode(
        payload.model_dump(),
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenPayload]:
    """Decode and validate a JWT token.
    
    Args:
        token: JWT token string.
        
    Returns:
        TokenPayload if valid, None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return TokenPayload(**payload)
    except JWTError:
        return None


def create_refresh_token(subject: str) -> str:
    """Create a refresh token with longer expiry.
    
    Args:
        subject: User ID.
        
    Returns:
        Encoded refresh JWT token.
    """
    expires_delta = timedelta(days=settings.refresh_token_expire_days)
    return create_access_token(subject, expires_delta=expires_delta, scopes=["refresh"])

