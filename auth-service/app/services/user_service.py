from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_email, create_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user_service(db: Session, email: str, password: str):
    # regra de negócio, náo permite email duplicado
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise Exception("Email já cadastrado")

    # hash da senha, passa a senha em testo e retorna a senha em hash
    hashed_password = pwd_context.hash(password)

    return create_user(db, email, hashed_password)