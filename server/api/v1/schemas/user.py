from uuid import UUID

from pydantic import BaseModel

from domain.entities.user import User
from domain.value_objects import Role


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: Role = Role.collector
    admin_key: str | None = None


class UserResponse(BaseModel):
    id: UUID
    username: str
    role: Role

    @classmethod
    def from_entity(cls, user: User) -> "UserResponse":
        return cls(id=user.id, username=user.username, role=user.role)
