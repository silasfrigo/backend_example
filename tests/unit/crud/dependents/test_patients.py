import pytest

from fastapi import HTTPException
from requests import Session
from requests.exceptions import ConnectionError

from prescriptions.utils import CacheHandler
from tests.fixtures import dependent_patient


def test_get_patient_cached(dependents, mocker, dynamodb):
    cache_handler = CacheHandler('patient_1')
    cache_handler.save_cache(dependent_patient, 60)
    assert dependents.get_patient('1') == dependent_patient


def test_get_patient_api(dependents, mocker, dynamodb, fake_request):
    fake_request.json_return = dependent_patient
    mocker.patch.object(Session, 'get', return_value=fake_request)
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    assert dependents.get_patient(1) == dependent_patient
    assert CacheHandler.save_cache.call_count == 1


def test_get_patient_api_not_found(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 404
    mocker.patch.object(Session, 'get', return_value=fake_request)
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    with pytest.raises(HTTPException):
        dependents.get_patient(1)

    assert CacheHandler.save_cache.call_count == 0


def test_get_patient_api_conn_error(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 500
    mocker.patch.object(Session, 'get', side_effect=ConnectionError())
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    with pytest.raises(HTTPException):
        dependents.get_patient(1)

    assert CacheHandler.save_cache.call_count == 0
