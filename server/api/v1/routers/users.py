from fastapi import APIRouter, Depends

from api.dependencies import get_current_user
from api.v1.schemas.user import UserResponse
from domain.entities.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.from_entity(current_user)
