import hashlib
import secrets
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[User]:
        return list(self.session.scalars(select(User).order_by(User.uid)).all())

    def get_by_id(self, uid: int) -> User | None:
        return self.session.get(User, uid)

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def get_by_username(self, username: str) -> User | None:
        return self.session.scalar(select(User).where(User.username == username))

    def create(self, user_data: dict[str, Any]) -> User:
        user_data = dict(user_data)
        user_data["password"] = self._hash_password(user_data["password"])
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, uid: int, user_data: dict[str, Any]) -> User | None:
        user = self.get_by_id(uid)
        if user is None:
            return None

        user_data = dict(user_data)
        if user_data.get("password") is not None:
            user_data["password"] = self._hash_password(user_data["password"])
        for field, value in user_data.items():
            setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, uid: int) -> User | None:
        user = self.get_by_id(uid)
        if user is None:
            return None

        self.session.delete(user)
        self.session.commit()
        return user

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = secrets.token_bytes(16)
        password_hash = hashlib.scrypt(
            password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=64
        )
        return f"scrypt$16384${salt.hex()}${password_hash.hex()}"