from aws_lambda_powertools import Logger

from prescriptions.crud.dependents import DependentsAPI
from prescriptions.schemas.prescription import CreatePrescription, ReadPrescription
from prescriptions.schemas.dependents import Clinic, Patient, Physician
from prescriptions.models.prescription import Prescription

from fastapi import HTTPException

logger = Logger(child=True)


class ProcessPrescription:
    def __init__(self, db):
        self.db = db

    def create(self, prescription):
        self.db.add(prescription)
        self.db.flush()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def process(self, prescription: CreatePrescription):
        prepared_prescription = self.prepare_data(prescription)
        self.create(prepared_prescription)
        metrics = self.create_metrics(prepared_prescription)
        self.send_metrics(metrics)
        self.commit()

        return ReadPrescription(id=prepared_prescription.id, **prescription.dict())

    def send_metrics(self, metrics):
        dependents_api = DependentsAPI()
        try:
            dependents_api.send_metrics(metrics)
        except HTTPException as err:
            self.rollback()
            raise err

    def prepare_data(self, data_in: CreatePrescription):
        prescriptions = self.parse_sql_data(data_in)
        return Prescription(**prescriptions)

    def create_metrics(self, prescription):
        dependents_api = DependentsAPI()
        try:
            physician = Physician(**dependents_api.get_physician(prescription.physician_id))
            clinic = dependents_api.get_clinic(prescription.clinic_id)
            patient = Patient(**dependents_api.get_patient(prescription.patient_id))
        except HTTPException as err:
            self.rollback()
            raise err

        metrics = {}
        metrics.update(physician.dict())
        if clinic:
            clinic = Clinic(**clinic)
            metrics.update(clinic.dict())
        metrics.update(patient.dict())
        return metrics

    def parse_sql_data(self, data_in):
        return {
            "clinic_id": data_in.clinic.id,
            "physician_id": data_in.physician.id,
            "patient_id": data_in.patient.id,
            "text": data_in.text,
        }
