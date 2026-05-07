from fastapi import APIRouter

from .routers.auth import router as auth_router
from .routers.collection import router as collection_router
from .routers.master_cards import router as master_cards_router
from .routers.users import router as users_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(master_cards_router)
router.include_router(collection_router)
