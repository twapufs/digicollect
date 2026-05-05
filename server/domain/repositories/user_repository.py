from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None: ...

    @abstractmethod
    def get(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def list(self) -> list[User]: ...

    @abstractmethod
    def update(self, user: User) -> None: ...

    @abstractmethod
    def delete(self, user_id: UUID) -> None: ...
