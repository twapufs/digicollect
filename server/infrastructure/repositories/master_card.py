from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.master_card import MasterCard
from domain.repositories.master_card_repository import AbstractMasterCardRepository
from domain.value_objects import Rarity
from infrastructure.models.master_card import MasterCardModel


class SqlAlchemyMasterCardRepository(AbstractMasterCardRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, card: MasterCard) -> None:
        self._session.add(self._to_model(card))

    def get(self, card_id: UUID) -> MasterCard | None:
        stmt = select(MasterCardModel).where(MasterCardModel.id == card_id)
        model = self._session.scalars(stmt).first()
        return self._to_entity(model) if model else None

    def list(self) -> list[MasterCard]:
        stmt = select(MasterCardModel)
        return [self._to_entity(m) for m in self._session.scalars(stmt)]

    def update(self, card: MasterCard) -> None:
        stmt = select(MasterCardModel).where(MasterCardModel.id == card.id)
        model = self._session.scalars(stmt).first()
        if model:
            model.title = card.title
            model.symbol = card.symbol
            model.rarity = card.rarity.value
            model.description = card.description
            model.quantity = card.quantity
            model.available_quantity = card.available_quantity

    def delete(self, card_id: UUID) -> None:
        stmt = select(MasterCardModel).where(MasterCardModel.id == card_id)
        model = self._session.scalars(stmt).first()
        if model:
            self._session.delete(model)

    def _to_entity(self, model: MasterCardModel) -> MasterCard:
        return MasterCard(
            id=model.id,
            title=model.title,
            symbol=model.symbol,
            rarity=Rarity(model.rarity),
            description=model.description,
            quantity=model.quantity,
            available_quantity=model.available_quantity,
        )

    def _to_model(self, entity: MasterCard) -> MasterCardModel:
        return MasterCardModel(
            id=entity.id,
            title=entity.title,
            symbol=entity.symbol,
            rarity=entity.rarity.value,
            description=entity.description,
            quantity=entity.quantity,
            available_quantity=entity.available_quantity,
        )
