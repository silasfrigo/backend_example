import pytest

from fastapi import HTTPException
from requests import Session
from requests.exceptions import ConnectionError

from prescriptions.utils import CacheHandler
from tests.fixtures import dependent_physician


def test_get_physician_cached(dependents, mocker, dynamodb):
    cache_handler = CacheHandler('physician_1')
    cache_handler.save_cache(dependent_physician, 60)
    assert dependents.get_physician('1') == dependent_physician


def test_get_physician_api(dependents, mocker, dynamodb, fake_request):
    fake_request.json_return = dependent_physician
    mocker.patch.object(Session, 'get', return_value=fake_request)
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    assert dependents.get_physician(1) == dependent_physician
    assert CacheHandler.save_cache.call_count == 1


def test_get_physician_api_not_found(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 404
    mocker.patch.object(Session, 'get', return_value=fake_request)
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    with pytest.raises(HTTPException):
        dependents.get_physician(1)

    assert CacheHandler.save_cache.call_count == 0


def test_get_physician_api_conn_error(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 500
    mocker.patch.object(Session, 'get', side_effect=ConnectionError())
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    with pytest.raises(HTTPException):
        dependents.get_physician(1)

    assert CacheHandler.save_cache.call_count == 0
