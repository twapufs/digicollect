import uuid
from dataclasses import dataclass, field

from ..value_objects import Role


@dataclass
class User:
    username: str
    hashed_password: str
    role: Role
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def create(cls, username: str, hashed_password: str, role: Role) -> "User":
        return cls(username=username, hashed_password=hashed_password, role=role)

    def is_admin(self) -> bool:
        return self.role == Role.admin

    def is_collector(self) -> bool:
        return self.role == Role.collector

    def update_username(self, username: str) -> None:
        self.username = username

    def update_password(self, hashed_password: str) -> None:
        self.hashed_password = hashed_password

    def update_role(self, role: Role) -> None:
        self.role = role
