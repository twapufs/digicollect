import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .master_card import MasterCard
from .user import User


@dataclass
class CollectedCard:
    master_card: MasterCard
    user: User
    collected_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def create(cls, master_card: MasterCard, user: User) -> "CollectedCard":
        master_card.collect()
        return cls(
            master_card=master_card,
            user=user,
            collected_at=datetime.now(timezone.utc),
        )

    def remove(self) -> None:
        self.master_card.return_card()
