from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from domain.entities.collected_card import CollectedCard
from domain.entities.master_card import MasterCard
from domain.entities.user import User
from domain.repositories.collected_card_repository import AbstractCollectedCardRepository
from domain.value_objects import Rarity, Role
from infrastructure.models.collected_card import CollectedCardModel


class SqlAlchemyCollectedCardRepository(AbstractCollectedCardRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, card: CollectedCard) -> None:
        from infrastructure.models.collected_card import CollectedCardModel

        model = CollectedCardModel(
            id=card.id,
            master_card_id=card.master_card.id,
            user_id=card.user.id,
            collected_at=card.collected_at,
        )
        self._session.add(model)

    def get(self, card_id: UUID) -> CollectedCard | None:
        stmt = (
            select(CollectedCardModel)
            .where(CollectedCardModel.id == card_id)
            .options(
                selectinload(CollectedCardModel.master_card),
                selectinload(CollectedCardModel.user),
            )
        )
        model = self._session.scalars(stmt).first()
        return self._to_entity(model) if model else None

    def list_by_user(self, user_id: UUID) -> list[CollectedCard]:
        stmt = (
            select(CollectedCardModel)
            .where(CollectedCardModel.user_id == user_id)
            .options(
                selectinload(CollectedCardModel.master_card),
                selectinload(CollectedCardModel.user),
            )
        )
        return [self._to_entity(m) for m in self._session.scalars(stmt)]

    def list_by_master_card(self, master_card_id: UUID) -> list[CollectedCard]:
        stmt = (
            select(CollectedCardModel)
            .where(CollectedCardModel.master_card_id == master_card_id)
            .options(
                selectinload(CollectedCardModel.master_card),
                selectinload(CollectedCardModel.user),
            )
        )
        return [self._to_entity(m) for m in self._session.scalars(stmt)]

    def delete(self, card_id: UUID) -> None:
        stmt = select(CollectedCardModel).where(CollectedCardModel.id == card_id)
        model = self._session.scalars(stmt).first()
        if model:
            self._session.delete(model)

    def _to_entity(self, model: CollectedCardModel) -> CollectedCard:
        master_card = MasterCard(
            id=model.master_card.id,
            title=model.master_card.title,
            symbol=model.master_card.symbol,
            rarity=Rarity(model.master_card.rarity),
            description=model.master_card.description,
            quantity=model.master_card.quantity,
            available_quantity=model.master_card.available_quantity,
        )
        user = User(
            id=model.user.id,
            username=model.user.username,
            hashed_password=model.user.hashed_password,
            role=Role(model.user.role),
        )
        return CollectedCard(
            id=model.id,
            master_card=master_card,
            user=user,
            collected_at=model.collected_at,
        )
