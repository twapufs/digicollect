from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.collected_card import CollectedCard


class AbstractCollectedCardRepository(ABC):
    @abstractmethod
    def add(self, card: CollectedCard) -> None: ...

    @abstractmethod
    def get(self, card_id: UUID) -> CollectedCard | None: ...

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> list[CollectedCard]: ...

    @abstractmethod
    def list_by_master_card(self, master_card_id: UUID) -> list[CollectedCard]: ...

    @abstractmethod
    def delete(self, card_id: UUID) -> None: ...
