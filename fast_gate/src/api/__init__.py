from fastapi import APIRouter

from .auth import router as auth_router
from .billing import router as billing_router
from .oauth import router as oauth_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(billing_router)
router.include_router(oauth_router)
