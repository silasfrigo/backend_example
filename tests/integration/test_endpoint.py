from ..fixtures import Fake, prescription, metrics

from prescriptions.crud.prescription import ProcessPrescription
from prescriptions.models.prescription import Prescription


def test_create_prescription(client, mocker):
    mocker.patch.object(ProcessPrescription, 'create', return_value=True)
    mocker.patch.object(ProcessPrescription, 'prepare_data', return_value=Prescription(**prescription))
    mocker.patch.object(ProcessPrescription, 'create_metrics', return_value=metrics)
    mocker.patch.object(ProcessPrescription, 'send_metrics', return_value=True)
    mocker.patch.object(ProcessPrescription, 'commit', return_value=Fake())

    response = client.post(
        'v1/prescriptions',
        headers={"Content-Type": "application/json"},
        json={
            'clinic': {
                'id': 2
            },
            'physician': {
                'id': 4
            },
            'patient': {
                'id': 6
            },
            'text': 'fake text'
        }
    )

    assert response.json() == {
        'data': {
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
    }
