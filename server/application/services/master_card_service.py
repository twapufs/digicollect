from uuid import UUID

from application.exceptions import MasterCardNotFoundError
from domain.entities.master_card import MasterCard
from domain.entities.user import User
from domain.exceptions import InsufficientPermissionsError
from domain.unit_of_work import AbstractUnitOfWork
from domain.value_objects import Rarity


class MasterCardService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    def create(
        self,
        actor: User,
        title: str,
        symbol: str,
        rarity: Rarity,
        description: str,
        quantity: int,
    ) -> MasterCard:
        if not actor.is_admin():
            raise InsufficientPermissionsError("Only admins can create master cards")
        card = MasterCard.create(title, symbol, rarity, description, quantity)
        self._uow.master_cards.add(card)
        self._uow.commit()
        return card

    def get(self, card_id: UUID) -> MasterCard:
        card = self._uow.master_cards.get(card_id)
        if not card:
            raise MasterCardNotFoundError(card_id)
        return card

    def list_all(self) -> list[MasterCard]:
        return self._uow.master_cards.list()

    def update(
        self,
        actor: User,
        card_id: UUID,
        title: str | None = None,
        symbol: str | None = None,
        rarity: Rarity | None = None,
        description: str | None = None,
        quantity: int | None = None,
    ) -> MasterCard:
        if not actor.is_admin():
            raise InsufficientPermissionsError("Only admins can update master cards")
        card = self._uow.master_cards.get(card_id)
        if not card:
            raise MasterCardNotFoundError(card_id)
        if title is not None:
            card.update_title(title)
        if symbol is not None:
            card.update_symbol(symbol)
        if rarity is not None:
            card.update_rarity(rarity)
        if description is not None:
            card.update_description(description)
        if quantity is not None:
            card.update_quantity(quantity)
        self._uow.master_cards.update(card)
        self._uow.commit()
        return card

    def delete(self, actor: User, card_id: UUID) -> None:
        if not actor.is_admin():
            raise InsufficientPermissionsError("Only admins can delete master cards")
        card = self._uow.master_cards.get(card_id)
        if not card:
            raise MasterCardNotFoundError(card_id)
        self._uow.master_cards.delete(card_id)
        self._uow.commit()
