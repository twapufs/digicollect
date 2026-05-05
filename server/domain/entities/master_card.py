import uuid
from dataclasses import dataclass, field

from ..value_objects import Rarity
from ..exceptions import CardNotAvailableError, InvalidQuantityError


@dataclass
class MasterCard:
    title: str
    symbol: str
    rarity: Rarity
    description: str
    quantity: int
    available_quantity: int
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def create(
        cls,
        title: str,
        symbol: str,
        rarity: Rarity,
        description: str,
        quantity: int,
    ) -> "MasterCard":
        if quantity < 0:
            raise InvalidQuantityError("Quantity must be non-negative")
        return cls(
            title=title,
            symbol=symbol,
            rarity=rarity,
            description=description,
            quantity=quantity,
            available_quantity=quantity,
        )

    def can_collect(self) -> bool:
        return self.available_quantity > 0

    def collect(self) -> None:
        if not self.can_collect():
            raise CardNotAvailableError(
                f"No available copies of '{self.title}'"
            )
        self.available_quantity -= 1

    def return_card(self) -> None:
        self.available_quantity += 1

    def update_title(self, title: str) -> None:
        self.title = title

    def update_symbol(self, symbol: str) -> None:
        self.symbol = symbol

    def update_rarity(self, rarity: Rarity) -> None:
        self.rarity = rarity

    def update_description(self, description: str) -> None:
        self.description = description

    def update_quantity(self, new_quantity: int) -> None:
        collected = self.quantity - self.available_quantity
        if new_quantity < collected:
            raise InvalidQuantityError(
                "Cannot reduce quantity below already-collected "
                f"count ({collected})"
            )
        self.available_quantity = new_quantity - collected
        self.quantity = new_quantity
