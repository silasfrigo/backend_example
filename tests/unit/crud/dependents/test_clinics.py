from requests import Session
from requests.exceptions import ConnectionError

from prescriptions.utils import CacheHandler
from tests.fixtures import dependent_clinic


def test_get_clinic_cached(dependents, mocker, dynamodb):
    cache_handler = CacheHandler('clinic_1')
    cache_handler.save_cache(dependent_clinic, 60)
    assert dependents.get_clinic('1') == dependent_clinic


def test_get_clinic_api(dependents, mocker, dynamodb, fake_request):
    fake_request.json_return = dependent_clinic
    mocker.patch.object(Session, 'get', return_value=fake_request)
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    assert dependents.get_clinic(1) == dependent_clinic
    assert CacheHandler.save_cache.call_count == 1


def test_get_clinic_api_404(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 404
    mocker.patch.object(Session, 'get', return_value=fake_request)
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    assert dependents.get_clinic(1) is None
    assert CacheHandler.save_cache.call_count == 0


def test_get_clinic_api_conn_error(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 500
    mocker.patch.object(Session, 'get', side_effect=ConnectionError())
    mocker.patch.object(CacheHandler, 'save_cache', return_value=True)

    assert dependents.get_clinic(1) is None
    assert CacheHandler.save_cache.call_count == 0
