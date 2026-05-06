import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base import Base
from .master_card import MasterCardModel
from .user import UserModel


class CollectedCardModel(Base):
    __tablename__ = "collected_cards"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    master_card_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("master_cards.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    master_card: Mapped[MasterCardModel] = relationship(back_populates="collected_cards")
    user: Mapped[UserModel] = relationship(back_populates="collected_cards")
