from fastapi import APIRouter

from .company import router as company_router
from .customer import router as customer_router

router = APIRouter()

router.include_router(company_router)
router.include_router(customer_router)
