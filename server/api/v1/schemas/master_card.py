from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.master_card import MasterCard
from domain.value_objects import Rarity


class CreateMasterCardRequest(BaseModel):
    title: str
    symbol: str
    rarity: Rarity
    description: str
    quantity: int = Field(ge=1)


class UpdateMasterCardRequest(BaseModel):
    title: str | None = None
    symbol: str | None = None
    rarity: Rarity | None = None
    description: str | None = None
    quantity: int | None = Field(default=None, ge=1)


class MasterCardResponse(BaseModel):
    id: UUID
    title: str
    symbol: str
    rarity: Rarity
    description: str
    quantity: int
    available_quantity: int

    @classmethod
    def from_entity(cls, card: MasterCard) -> "MasterCardResponse":
        return cls(
            id=card.id,
            title=card.title,
            symbol=card.symbol,
            rarity=card.rarity,
            description=card.description,
            quantity=card.quantity,
            available_quantity=card.available_quantity,
        )
