import pytest
import json

from prescriptions.utils import CacheHandler
from cache import file_cache


@pytest.fixture
def cache_handler():
    cache_handler = CacheHandler(
        cache_key='fake_key'
    )
    yield cache_handler


def test_get_cache(cache_handler, mocker, dynamodb):
    mocker.patch.object(CacheHandler, '_get_cache_from_dynamo', return_vale={'from': 'dynamo'})

    file_cache.set(key='fake_key', value=json.dumps({'from': 'file'}))

    assert cache_handler.get_cache() == {'from': 'file'}
    assert CacheHandler._get_cache_from_dynamo.call_count == 0


def test_get_dynamo(cache_handler, mocker, dynamodb):
    cache_handler.cache_ttl = 3600 * 24
    cache_handler._save_cache_dynamo(json.dumps({'foo': 'bar'}))

    assert cache_handler.get_cache() == {'foo': 'bar'}

    cache_handler._get_cache_from_dynamo() == {'foo': 'bar'}
    cache_handler._get_cache_from_file() == {'foo': 'bar'}


def test_save_cache(cache_handler, mocker, dynamodb):
    mocker.patch.object(CacheHandler, '_save_cache_file', return_vale={'foo': 'bar'})
    mocker.patch.object(CacheHandler, '_save_cache_dynamo', return_vale={'foo': 'bar'})

    assert cache_handler.save_cache('fake_value', 3600 * 12)
