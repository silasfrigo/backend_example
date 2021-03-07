import pytest

from prescriptions.crud.prescription import ProcessPrescription
from prescriptions.schemas.prescription import CreatePrescription
from prescriptions.models.prescription import Prescription
from ..fixtures import metrics, prescription, Fake


@pytest.fixture
def create_prescription():
    return CreatePrescription(clinic={'id': 2}, physician={'id': 4}, patient={'id': 6}, text='fake text')


@pytest.fixture
def process_prescription():
    return ProcessPrescription(db=Fake())


def test_process(mocker, create_prescription, process_prescription):
    mocker.patch.object(ProcessPrescription, 'create', return_value=True)
    mocker.patch.object(ProcessPrescription, 'prepare_data', return_value=Prescription(**prescription))
    mocker.patch.object(ProcessPrescription, 'create_metrics', return_value=metrics)
    mocker.patch.object(ProcessPrescription, 'send_metrics', return_value=True)
    mocker.patch.object(ProcessPrescription, 'commit', return_value=Fake())

    processed_prescription = process_prescription.process(create_prescription)
    assert processed_prescription.dict() == {
        'clinic': {
            'id': 2
        },
        'physician': {
            'id': 4
        },
        'patient': {
            'id': 6
        },
        'text': 'fake text',
        'id': 1
    }
