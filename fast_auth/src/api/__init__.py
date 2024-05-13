from fastapi import APIRouter

from .company_auth import router as company_auth_router
from .customer_auth import router as customer_auth_router
from .oauth2 import router as oauth2_router

router = APIRouter()

router.include_router(company_auth_router)
router.include_router(customer_auth_router)
router.include_router(oauth2_router)
