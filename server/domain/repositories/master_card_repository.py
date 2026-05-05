from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.master_card import MasterCard


class AbstractMasterCardRepository(ABC):
    @abstractmethod
    def add(self, card: MasterCard) -> None: ...

    @abstractmethod
    def get(self, card_id: UUID) -> MasterCard | None: ...

    @abstractmethod
    def list(self) -> list[MasterCard]: ...

    @abstractmethod
    def update(self, card: MasterCard) -> None: ...

    @abstractmethod
    def delete(self, card_id: UUID) -> None: ...
