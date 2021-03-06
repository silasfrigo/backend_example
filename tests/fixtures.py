dependent_physician = {
    "id": "5",
    "name": "Kassandra Feil",
    "crm": "6c11e33b-3b51-4f28-a1a1-f5f97b3d83e0"
}


dependent_clinic = {
    "id": "1",
    "name": "Elenor Mraz"
}


dependent_patient = {
    "id": "1",
    "name": "Vita Mante",
    "email": "Herta38@hotmail.com",
    "phone": "702.043.4233 x475"
}


dependent_metrics = {
    "id": "1",
    "clinic_id": 1,
    "clinic_name": "Clinica A",
    "physician_id": 1,
    "physician_name": "Dr. João",
    "physician_crm": "SP293893",
    "patient_id": 1,
    "patient_name": "Rodrigo",
    "patient_email": "rodrigo@gmail.com",
    "patient_phone": "(16)998765625"
}


metrics = {
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


prescription = {
    'id': 1,
    'clinic_id': 2,
    'patient_id': 3,
    'physician_id': 4,
    'text': 'fake text'
}


class Fake:

    def rollback(self):
        return True

    def commit(self):
        return True


class FakeRequest:
    json_return = {'foo': 'bar'}
    status_code_return = 200

    @property
    def status_code(self):
        return self.status_code_return

    def json(self):
        return self.json_return
