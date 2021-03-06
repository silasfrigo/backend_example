from fastapi import APIRouter
from .endpoints.prescription import router as prescription_router


router = APIRouter()
router.include_router(prescription_router, tags=['prescriptions'])
