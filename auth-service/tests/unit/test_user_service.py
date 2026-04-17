from uuid import uuid4

import pytest

from app.core.exceptions import AuthenticationError, DuplicateEmailError
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.services.user_service import authenticate_user, register_user
from app.schemas.user import LoginRequest, UserRegisterRequest


class DummySession:
    def __init__(self):
        self.added_objects = []
        self.committed = False
        self.refreshed = False

    def add(self, obj):
        self.added_objects.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, _obj):
        self.refreshed = True


def test_register_user_rejects_duplicate_email(monkeypatch) -> None:
    payload = UserRegisterRequest(
        full_name="Jane Doe",
        email="jane@example.com",
        password="StrongPass123",
    )

    monkeypatch.setattr(
        "app.services.user_service.get_user_by_email",
        lambda _session, _email: User(
            id=uuid4(),
            full_name="Existing User",
            email="jane@example.com",
            password_hash="hashed",
            role=UserRole.USER,
            is_active=True,
        ),
    )

    with pytest.raises(DuplicateEmailError, match="Email já cadastrado"):
        register_user(DummySession(), payload)


def test_authenticate_user_returns_access_token(monkeypatch) -> None:
    session = DummySession()
    user = User(
        id=uuid4(),
        full_name="Jane Doe",
        email="jane@example.com",
        password_hash=hash_password("SuperSecret123"),
        role=UserRole.USER,
        is_active=True,
    )

    monkeypatch.setattr(
        "app.services.user_service.get_user_by_email",
        lambda _session, _email: user,
    )

    response = authenticate_user(
        session,
        LoginRequest(email="jane@example.com", password="SuperSecret123"),
    )

    assert response.access_token
    assert response.token_type == "bearer"
    assert response.expires_in > 0


def test_authenticate_user_rejects_invalid_password(monkeypatch) -> None:
    session = DummySession()
    user = User(
        id=uuid4(),
        full_name="Jane Doe",
        email="jane@example.com",
        password_hash=hash_password("SuperSecret123"),
        role=UserRole.USER,
        is_active=True,
    )

    monkeypatch.setattr(
        "app.services.user_service.get_user_by_email",
        lambda _session, _email: user,
    )

    with pytest.raises(AuthenticationError, match="Email ou senha inválidos"):
        authenticate_user(
            session,
            LoginRequest(email="jane@example.com", password="WrongPassword123"),
        )
