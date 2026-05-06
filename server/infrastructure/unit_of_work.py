from types import TracebackType
from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from domain.unit_of_work import AbstractUnitOfWork
from infrastructure.repositories import (
    SqlAlchemyCollectedCardRepository,
    SqlAlchemyMasterCardRepository,
    SqlAlchemyUserRepository,
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> Self:
        self._session: Session = self._session_factory()
        self.users = SqlAlchemyUserRepository(self._session)
        self.master_cards = SqlAlchemyMasterCardRepository(self._session)
        self.collected_cards = SqlAlchemyCollectedCardRepository(self._session)
        return super().__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
