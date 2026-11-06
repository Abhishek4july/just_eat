import pytest
from jose import jwt

from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token, verify_access_token
from app.config import settings, Settings


# ---------------- Security Tests ----------------

def test_hash_password_returns_different_string():
    password = "password123"
    hashed = hash_password(password)

    assert hashed != password


def test_hash_password_returns_string():
    hashed = hash_password("password123")

    assert isinstance(hashed, str)


def test_verify_correct_password():
    password = "password123"
    hashed = hash_password(password)

    assert verify_password(password, hashed)


def test_verify_wrong_password():
    password = "password123"
    hashed = hash_password(password)

    assert not verify_password("wrongpassword", hashed)


# ---------------- JWT Tests ----------------

def test_create_access_token_returns_string():
    token = create_access_token({"sub": "test@example.com"})

    assert isinstance(token, str)


def test_access_token_has_three_parts():
    token = create_access_token({"sub": "test@example.com"})

    assert len(token.split(".")) == 3


def test_verify_access_token_returns_payload():
    token = create_access_token({"sub": "test@example.com"})

    payload = verify_access_token(token)

    assert payload["sub"] == "test@example.com"


def test_verify_invalid_token_returns_none():
    payload = verify_access_token("this.is.not.valid")

    assert payload is None


# ---------------- Config Tests ----------------

def test_settings_instance_created():
    assert isinstance(settings, Settings)


def test_secret_key_not_empty():
    assert settings.SECRET_KEY != ""