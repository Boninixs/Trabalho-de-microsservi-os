from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repository import get_user_by_id
from app.schemas.user import TokenClaims

security = HTTPBearer(auto_error=False)


def get_current_token_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> TokenClaims:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais não fornecidas",
        )

    try:
        return decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


def get_current_user(
    claims: TokenClaims = Depends(get_current_token_claims),
    db: Session = Depends(get_db),
) -> User:
    user = get_user_by_id(db, claims.subject)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário do token não encontrado",
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
        )

    return current_user


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    allowed_roles = {role.value for role in roles}

    def dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado para o perfil informado",
            )

        return current_user

    return dependency
