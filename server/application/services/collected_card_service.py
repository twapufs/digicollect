from uuid import UUID

from application.exceptions import CollectedCardNotFoundError, MasterCardNotFoundError
from domain.entities.collected_card import CollectedCard
from domain.entities.user import User
from domain.exceptions import InsufficientPermissionsError
from domain.unit_of_work import AbstractUnitOfWork


class CollectedCardService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    def collect(self, actor: User, master_card_id: UUID) -> CollectedCard:
        if not actor.is_collector():
            raise InsufficientPermissionsError("Only collectors can collect cards")
        master_card = self._uow.master_cards.get(master_card_id)
        if not master_card:
            raise MasterCardNotFoundError(master_card_id)
        # CollectedCard.create calls master_card.collect(), raising CardNotAvailableError if exhausted
        collected = CollectedCard.create(master_card, actor)
        self._uow.collected_cards.add(collected)
        self._uow.master_cards.update(master_card)
        self._uow.commit()
        return collected

    def remove(self, actor: User, collected_card_id: UUID) -> None:
        if not actor.is_collector():
            raise InsufficientPermissionsError("Only collectors can remove cards")
        card = self._uow.collected_cards.get(collected_card_id)
        if not card:
            raise CollectedCardNotFoundError(collected_card_id)
        if card.user.id != actor.id:
            raise InsufficientPermissionsError("You can only remove cards from your own collection")
        card.remove()
        self._uow.master_cards.update(card.master_card)
        self._uow.collected_cards.delete(collected_card_id)
        self._uow.commit()

    def list_my_collection(self, actor: User) -> list[CollectedCard]:
        if not actor.is_collector():
            raise InsufficientPermissionsError("Only collectors have a collection")
        return self._uow.collected_cards.list_by_user(actor.id)
