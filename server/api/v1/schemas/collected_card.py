from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from api.v1.schemas.master_card import MasterCardResponse
from domain.entities.collected_card import CollectedCard


class CollectCardRequest(BaseModel):
    master_card_id: UUID


class CollectedCardResponse(BaseModel):
    id: UUID
    master_card: MasterCardResponse
    collected_at: datetime

    @classmethod
    def from_entity(cls, card: CollectedCard) -> "CollectedCardResponse":
        return cls(
            id=card.id,
            master_card=MasterCardResponse.from_entity(card.master_card),
            collected_at=card.collected_at,
        )
