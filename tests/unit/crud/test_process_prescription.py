import pytest

from fastapi import HTTPException
from prescriptions.crud.prescription import ProcessPrescription
from prescriptions.schemas.prescription import CreatePrescription
from prescriptions.crud.dependents import DependentsAPI
from ...fixtures import dependent_physician, dependent_patient, dependent_clinic, Fake


@pytest.fixture
def create_prescription():
    return CreatePrescription(clinic={'id': 2}, physician={'id': 4}, patient={'id': 6}, text='fake text')


@pytest.fixture
def process_prescription():
    return ProcessPrescription(db=Fake())


def test_parse_sql_data(process_prescription, create_prescription):
    prepared_data = process_prescription.parse_sql_data(create_prescription)
    assert prepared_data == {
        "clinic_id": create_prescription.clinic.id,
        "physician_id": create_prescription.physician.id,
        "patient_id": create_prescription.patient.id,
        "text": create_prescription.text,
    }


def test_prepare_data(process_prescription, create_prescription):
    prepared_data = process_prescription.prepare_data(create_prescription)
    assert prepared_data
    assert prepared_data.clinic_id == create_prescription.clinic.id
    assert prepared_data.patient_id == create_prescription.patient.id
    assert prepared_data.physician_id == create_prescription.physician.id
    assert prepared_data.text == create_prescription.text
    assert prepared_data.id is None


def test_create_metrics(process_prescription, create_prescription, mocker):
    mocker.patch.object(DependentsAPI, 'get_physician', return_value=dependent_physician)
    mocker.patch.object(DependentsAPI, 'get_clinic', return_value=dependent_clinic)
    mocker.patch.object(DependentsAPI, 'get_patient', return_value=dependent_patient)
    prescription = process_prescription.prepare_data(create_prescription)
    metrics = process_prescription.create_metrics(prescription)
    assert metrics == {
        'physician_id': 5,
        'physician_name': 'Kassandra Feil',
        'physician_crm': '6c11e33b-3b51-4f28-a1a1-f5f97b3d83e0',
        'clinic_id': 1,
        'clinic_name': 'Elenor Mraz',
        'patient_id': 1,
        'patient_name': 'Vita Mante',
        'patient_email': 'Herta38@hotmail.com',
        'patient_phone': '702.043.4233 x475'
    }

    mocker.patch.object(DependentsAPI, 'get_physician', side_effect=HTTPException(status_code=400))
    with pytest.raises(HTTPException):
        process_prescription.create_metrics(prescription)


def test_send_metrics(process_prescription, mocker):
    mocker.patch.object(DependentsAPI, 'send_metrics', return_value=True)
    process_prescription.send_metrics({})
    assert DependentsAPI.send_metrics.call_count == 1

    mocker.patch.object(DependentsAPI, 'send_metrics', side_effect=HTTPException(status_code=400))
    with pytest.raises(HTTPException):
        process_prescription.send_metrics({})
