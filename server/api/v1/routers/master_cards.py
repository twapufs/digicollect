from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_master_card_service, require_admin
from api.v1.schemas.master_card import (
    CreateMasterCardRequest,
    MasterCardResponse,
    UpdateMasterCardRequest,
)
from application.exceptions import MasterCardNotFoundError
from application.services.master_card_service import MasterCardService
from domain.entities.user import User
from domain.exceptions import InvalidQuantityError

router = APIRouter(prefix="/master-cards", tags=["master-cards"])


@router.post("/", response_model=MasterCardResponse, status_code=status.HTTP_201_CREATED)
def create_master_card(
    body: CreateMasterCardRequest,
    current_user: User = Depends(require_admin),
    service: MasterCardService = Depends(get_master_card_service),
) -> MasterCardResponse:
    card = service.create(
        current_user,
        body.title,
        body.symbol,
        body.rarity,
        body.description,
        body.quantity,
    )
    return MasterCardResponse.from_entity(card)


@router.get("/", response_model=list[MasterCardResponse])
def list_master_cards(
    current_user: User = Depends(require_admin),
    service: MasterCardService = Depends(get_master_card_service),
) -> list[MasterCardResponse]:
    return [MasterCardResponse.from_entity(c) for c in service.list_all(current_user)]


@router.get("/{card_id}", response_model=MasterCardResponse)
def get_master_card(
    card_id: UUID,
    current_user: User = Depends(require_admin),
    service: MasterCardService = Depends(get_master_card_service),
) -> MasterCardResponse:
    try:
        card = service.get(current_user, card_id)
    except MasterCardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return MasterCardResponse.from_entity(card)


@router.patch("/{card_id}", response_model=MasterCardResponse)
def update_master_card(
    card_id: UUID,
    body: UpdateMasterCardRequest,
    current_user: User = Depends(require_admin),
    service: MasterCardService = Depends(get_master_card_service),
) -> MasterCardResponse:
    try:
        card = service.update(current_user, card_id, **body.model_dump(exclude_unset=True))
    except MasterCardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidQuantityError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return MasterCardResponse.from_entity(card)


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_master_card(
    card_id: UUID,
    current_user: User = Depends(require_admin),
    service: MasterCardService = Depends(get_master_card_service),
) -> None:
    try:
        service.delete(current_user, card_id)
    except MasterCardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
