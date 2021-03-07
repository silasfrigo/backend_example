from aws_lambda_powertools import Logger
from fastapi import APIRouter, Depends
from prescriptions.schemas.prescription import CreatePrescription, ReadPrescription
from prescriptions.schemas.base import Result
from sqlalchemy.orm import Session
from prescriptions.get_db import get_db
from prescriptions.crud.prescription import ProcessPrescription


logger = Logger()
router = APIRouter()


@router.post('/prescriptions', response_model=Result[ReadPrescription])
async def create_prescription(prescription_in: CreatePrescription, db: Session = Depends(get_db)):
    process_prescription = ProcessPrescription(db=db)
    created = process_prescription.process(prescription_in)
    logger.info({'info': 'prescription_created_successfully', 'attr': created.__dict__})
    return {
        "data": created
    }
