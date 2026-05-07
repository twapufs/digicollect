from functools import lru_cache
from typing import Generator

import infrastructure.models  # noqa: F401 — registers ORM models with Base.metadata
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from application.exceptions import InvalidTokenError, TokenExpiredError
from application.services.collected_card_service import CollectedCardService
from application.services.master_card_service import MasterCardService
from application.services.user_service import UserService
from core.config import settings
from domain.entities.user import User
from domain.unit_of_work import AbstractUnitOfWork
from infrastructure.database import build_session_factory
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


@lru_cache
def _session_factory():
    return build_session_factory(settings.database_url, settings.auto_db_init)


def get_uow() -> Generator[AbstractUnitOfWork, None, None]:
    uow = SqlAlchemyUnitOfWork(_session_factory())
    with uow:
        yield uow


def get_user_service(uow: AbstractUnitOfWork = Depends(get_uow)) -> UserService:
    return UserService(uow)


def get_master_card_service(uow: AbstractUnitOfWork = Depends(get_uow)) -> MasterCardService:
    return MasterCardService(uow)


def get_collected_card_service(uow: AbstractUnitOfWork = Depends(get_uow)) -> CollectedCardService:
    return CollectedCardService(uow)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> User:
    try:
        return service.authenticate(token)
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def require_collector(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_collector():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Collector access required",
        )
    return current_user
