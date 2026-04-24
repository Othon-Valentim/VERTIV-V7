"""
VERTIV v6.0 - Authentication & Authorization Module
Integrates with Supabase JWT for secure API access.
"""

import os
from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from functools import lru_cache

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nutilcpmpapjowqmxoqf.supabase.co")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")

# Security scheme
security = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
    """Decoded JWT token payload from Supabase"""
    sub: str  # User ID
    email: Optional[str] = None
    role: str = "authenticated"
    aud: str = "authenticated"
    exp: int = 0
    iat: int = 0


class CurrentUser(BaseModel):
    """Current authenticated user"""
    id: str
    email: Optional[str] = None
    role: str = "authenticated"


@lru_cache(maxsize=1)
def get_supabase_jwt_secret() -> str:
    """
    Get Supabase JWT secret from environment.
    In production, this should be the JWT secret from Supabase dashboard.
    """
    secret = os.getenv("SUPABASE_JWT_SECRET")
    if not secret:
        raise RuntimeError("SUPABASE_JWT_SECRET must be set for JWT verification.")
    return secret


def verify_supabase_token(token: str) -> TokenPayload:
    """
    Verify a Supabase JWT token.

    Args:
        token: The JWT token from Authorization header

    Returns:
        TokenPayload with user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        secret = get_supabase_jwt_secret()

        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            audience="authenticated"
        )

        if not payload.get("sub"):
            raise jwt.InvalidTokenError("Missing subject claim")

        return TokenPayload(
            sub=payload.get("sub", ""),
            email=payload.get("email"),
            role=payload.get("role", "authenticated"),
            aud=payload.get("aud", "authenticated"),
            exp=payload.get("exp", 0),
            iat=payload.get("iat", 0)
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired. Please login again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> CurrentUser:
    """
    Dependency to get the current authenticated user.

    Usage:
        @app.get("/protected")
        async def protected_route(user: CurrentUser = Depends(get_current_user)):
            return {"user_id": user.id}
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_payload = verify_supabase_token(credentials.credentials)

    return CurrentUser(
        id=token_payload.sub,
        email=token_payload.email,
        role=token_payload.role
    )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[CurrentUser]:
    """
    Dependency to optionally get the current user.
    Returns None if no valid token is provided.

    Usage:
        @app.get("/public-or-private")
        async def route(user: Optional[CurrentUser] = Depends(get_optional_user)):
            if user:
                return {"message": f"Hello {user.email}"}
            return {"message": "Hello anonymous"}
    """
    if not credentials:
        return None

    try:
        token_payload = verify_supabase_token(credentials.credentials)
        return CurrentUser(
            id=token_payload.sub,
            email=token_payload.email,
            role=token_payload.role
        )
    except HTTPException:
        return None


def require_role(required_role: str):
    """
    Dependency factory to require a specific role.

    Usage:
        @app.get("/admin-only")
        async def admin_route(user: CurrentUser = Depends(require_role("admin"))):
            return {"message": "Admin access granted"}
    """
    async def role_checker(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if user.role != required_role and user.role != "service_role":
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role: {required_role}"
            )
        return user
    return role_checker


async def get_user_from_token_param(token: Optional[str] = None) -> CurrentUser:
    """
    Autentica usuário via query parameter.

    Necessário para SSE (Server-Sent Events) que não suporta headers customizados.

    Usage:
        @app.get("/stream")
        async def sse_endpoint(user: CurrentUser = Depends(get_user_from_token_param)):
            ...

    Segurança:
        - Token é passado via HTTPS (criptografado)
        - Token tem curta duração (Supabase default: 1 hora)
        - Não é logado em access logs (query params são omitidos)
    """
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide token parameter.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_payload = verify_supabase_token(token)

    return CurrentUser(
        id=token_payload.sub,
        email=token_payload.email,
        role=token_payload.role
    )
