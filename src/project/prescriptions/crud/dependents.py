import requests
from requests.exceptions import ConnectionError
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from aws_lambda_powertools import Logger
from prescriptions.config import settings

from fastapi import HTTPException

logger = Logger(child=True)

s = requests.Session()

physician = Retry(total=0, backoff_factor=0.1)
clinic = Retry(total=3, backoff_factor=0.1)
patient = Retry(total=2, backoff_factor=0.1)
metrics = Retry(total=5, backoff_factor=0.1)


class DependentsAPI:
    def __init__(self):
        self.base_url = 'https://5f71da6964a3720016e60ff8.mockapi.io/v1'

    def get_physician(self, physician_id):
        s.mount('https://', HTTPAdapter(max_retries=physician))
        try:
            response = s.get(f'{self.base_url}/physicians/{physician_id}', timeout=4, headers={'authentication': settings.physician_auth})
            if response.status_code == 200:
                # TODO: save to cache
                return response.json()
            else:
                if response.status_code == 404:
                    error = {'message': 'physician not found', 'code': 2}
        except ConnectionError:
            error = {'message': 'physicians service not available', 'code': 5}

        logger.info({'error': 'get_physician_failure', 'attr': error})
        raise HTTPException(status_code=400, detail=error or {})

    def get_clinic(self, clinic_id):
        s.mount('https://', HTTPAdapter(max_retries=clinic))
        # get_cache('clinic_'+ clinic_id)
        try:
            response = s.get(f'{self.base_url}/clinics/{clinic_id}', timeout=5, headers={'authentication': settings.clinic_auth})
            if response.status_code == 200:
                # save_cache('clinic_'+ clinic_id)
                # TODO: save to cache
                return response.json()

        except ConnectionError:
            logger.info({'error': 'get_clinic_failure'})

        return None

    def get_patient(self, patient_id):
        s.mount('https://', HTTPAdapter(max_retries=patient))
        try:
            response = s.get(f'{self.base_url}/patients/{patient_id}', timeout=3, headers={'authentication': settings.patient_auth})
            if response.status_code == 200:
                # TODO: save to cache
                return response.json()
            else:
                if response.status_code == 404:
                    error = {'message': 'patient not found', 'code': 3}
        except ConnectionError:
            error = {'message': 'patients service not available', 'code': 6}

        logger.info({'error': 'get_patient_failure', 'attr': error})
        raise HTTPException(status_code=400, detail=error or {})

    def send_metrics(self, data):
        s.mount('https://', HTTPAdapter(max_retries=metrics))
        try:
            response = s.post(f'{self.base_url}/metrics', timeout=6, headers={'authentication': settings.metric_auth}, data=data)
            if response.status_code == 201:
                return True
            else:
                error = {'message': 'metrics service not available', 'code': 4}
        except HTTPException:
            error = {'message': 'metrics service not available', 'code': 4}

        logger.info({'error': 'send_metrics_failure', 'attr': error})
        raise HTTPException(status_code=400, detail=error or {})
