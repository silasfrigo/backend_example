from prescriptions.schemas.prescription import CreatePrescription
from prescriptions.schemas.dependents import Clinic, Patient, Physician


def test_simple():
    assert CreatePrescription(clinic={'id': 1}, physician={'id': 1}, patient={'id': 1}, text='abc')


def test_validator():
    clinic = Clinic(id=1, name='fake clinic')
    assert clinic.clinic_name
    assert clinic.clinic_id

    patient = Patient(id=1, name='fake clinic', email='fake@test.com', phone='+5519988884444')
    assert patient.patient_name
    assert patient.patient_id
    assert patient.patient_phone
    assert patient.patient_email

    physician = Physician(id=1, name='fake clinic', crm='123123')
    assert physician.physician_crm
