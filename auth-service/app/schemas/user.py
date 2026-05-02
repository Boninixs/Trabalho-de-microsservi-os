""""
Esse arquivo é responsável por definir os esquemas de dados relacionados a usuários, 
incluindo solicitações de registro e login, respostas de token e perfil do usuário. 
Ele utiliza o Pydantic para validação e serialização dos dados.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserRegisterRequest(BaseModel):
    """"
    O UserRegisterRequest é um modelo de dados que representa a solicitação de registro de um novo usuário,
    incluindo o nome completo, email e senha do usuário.
    """
    full_name: str = Field(min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """"
    O LoginRequest é um modelo de dados que representa a solicitação de login de um usuário,
    incluindo o email e senha do usuário.
    """
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    """"
    O TokenResponse é um modelo de dados que representa a resposta contendo o token de acesso.
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenClaims(BaseModel):
    """"
    O TokenClaims é um modelo de dados que representa as reclamações contidas no token de acesso.
    """
    sub: UUID
    role: UserRole
    exp: int

    @property
    def subject(self) -> UUID:
        return self.sub


class UserProfileResponse(BaseModel):
    """"
    O UserProfileResponse é um modelo de dados que representa a resposta contendo as informações do perfil do usuário,
    incluindo ID, nome completo, email, função, status de ativação e datas de criação e atualização.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
