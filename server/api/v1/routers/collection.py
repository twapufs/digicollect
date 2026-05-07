from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_collected_card_service, require_collector
from api.v1.schemas.collected_card import CollectCardRequest, CollectedCardResponse
from application.exceptions import CollectedCardNotFoundError, MasterCardNotFoundError
from application.services.collected_card_service import CollectedCardService
from domain.entities.user import User
from domain.exceptions import CardNotAvailableError

router = APIRouter(prefix="/collection", tags=["collection"])


@router.post("/", response_model=CollectedCardResponse, status_code=status.HTTP_201_CREATED)
def collect_card(
    body: CollectCardRequest,
    current_user: User = Depends(require_collector),
    service: CollectedCardService = Depends(get_collected_card_service),
) -> CollectedCardResponse:
    try:
        card = service.collect(current_user, body.master_card_id)
    except MasterCardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except CardNotAvailableError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return CollectedCardResponse.from_entity(card)


@router.get("/", response_model=list[CollectedCardResponse])
def list_my_collection(
    current_user: User = Depends(require_collector),
    service: CollectedCardService = Depends(get_collected_card_service),
) -> list[CollectedCardResponse]:
    return [CollectedCardResponse.from_entity(c) for c in service.list_my_collection(current_user)]


@router.delete("/{collected_card_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_collected_card(
    collected_card_id: UUID,
    current_user: User = Depends(require_collector),
    service: CollectedCardService = Depends(get_collected_card_service),
) -> None:
    try:
        service.remove(current_user, collected_card_id)
    except CollectedCardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
