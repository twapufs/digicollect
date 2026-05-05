from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from .repositories import (
    AbstractCollectedCardRepository,
    AbstractMasterCardRepository,
    AbstractUserRepository,
)


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepository
    master_cards: AbstractMasterCardRepository
    collected_cards: AbstractCollectedCardRepository

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            self.rollback()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
