from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.repositories.user_repository import AbstractUserRepository
from domain.value_objects import Role
from infrastructure.models.user import UserModel


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, user: User) -> None:
        self._session.add(self._to_model(user))

    def get(self, user_id: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        model = self._session.scalars(stmt).first()
        return self._to_entity(model) if model else None

    def get_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        model = self._session.scalars(stmt).first()
        return self._to_entity(model) if model else None

    def list(self) -> list[User]:
        stmt = select(UserModel)
        return [self._to_entity(m) for m in self._session.scalars(stmt)]

    def update(self, user: User) -> None:
        stmt = select(UserModel).where(UserModel.id == user.id)
        model = self._session.scalars(stmt).first()
        if model:
            model.username = user.username
            model.hashed_password = user.hashed_password
            model.role = user.role.value

    def delete(self, user_id: UUID) -> None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        model = self._session.scalars(stmt).first()
        if model:
            self._session.delete(model)

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            hashed_password=model.hashed_password,
            role=Role(model.role),
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            hashed_password=entity.hashed_password,
            role=entity.role.value,
        )
