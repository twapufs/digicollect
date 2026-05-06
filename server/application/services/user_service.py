from uuid import UUID

import jwt

from application.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    TokenExpiredError,
    UserAlreadyExistsError,
)
from core.security import create_access_token, decode_access_token, hash_password, verify_password
from domain.entities.user import User
from domain.unit_of_work import AbstractUnitOfWork
from domain.value_objects import Role


class UserService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    def register(self, username: str, password: str, role: Role = Role.collector) -> User:
        if self._uow.users.get_by_username(username):
            raise UserAlreadyExistsError(username)
        user = User.create(username, hash_password(password), role)
        self._uow.users.add(user)
        self._uow.commit()
        return user

    def login(self, username: str, password: str) -> str:
        user = self._uow.users.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        return create_access_token(user.id)

    def authenticate(self, token: str) -> User:
        try:
            payload = decode_access_token(token)
            user_id = UUID(payload["sub"])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except (jwt.PyJWTError, KeyError, ValueError):
            raise InvalidTokenError()
        user = self._uow.users.get(user_id)
        if not user:
            raise InvalidTokenError()
        return user
