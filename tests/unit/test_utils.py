import pytest
import datetime
import pytz

from freezegun import freeze_time

from prescriptions.utils import CacheHandler
from cache import file_cache


@pytest.fixture
def cache_handler():
    cache_handler = CacheHandler(
        cache_key='fake_key'
    )
    yield cache_handler


def test_get_cache_from_file_empty(cache_handler):
    assert cache_handler._get_cache_from_file() is None


@freeze_time(datetime.datetime(2020, 1, 1, 00, 00, tzinfo=pytz.utc).isoformat())
def test_get_cache_from_file(cache_handler):
    file_cache.set('fake_key', '321123', expire=82800)

    assert cache_handler._get_cache_from_file() == '321123'
    assert cache_handler.max_age == 82800

    file_cache.pop('fake_key')
    assert cache_handler._get_cache_from_file() is None


def test_save_file(cache_handler):
    assert cache_handler._get_cache_from_file() is None

    cache_handler._save_cache_file('321123')
    assert cache_handler._get_cache_from_file() == '321123'

    file_cache.pop('fake_key', expire_time=True)


def test_get_expiration_time(cache_handler):
    cache_handler.cache_ttl = 3600 * 12
    dt = datetime.datetime(2020, 10, 17, 13, 00)
    dt = datetime.datetime.now().replace(microsecond=0)
    expiration_time = cache_handler._get_expiration_time(dt)

    dt_incremented = dt + datetime.timedelta(minutes=720)
    assert datetime.datetime.fromtimestamp(expiration_time) == dt_incremented


@freeze_time(datetime.datetime(2020, 1, 1, 00, 00, tzinfo=pytz.utc).isoformat())
def test_save_dynamo(dynamodb, cache_handler, mocker):
    date = datetime.datetime(2020, 1, 1, 23, 00, tzinfo=pytz.utc)
    mocker.patch.object(CacheHandler, '_get_expiration_time', return_value=int(date.timestamp()))

    assert cache_handler._save_cache_dynamo('123321')['ResponseMetadata']['HTTPStatusCode'] == 200
    assert cache_handler.max_age == 82800


@freeze_time(datetime.datetime(2020, 1, 1, 00, 00, tzinfo=pytz.utc).isoformat())
def test_get_cache_from_dynamo(dynamodb, cache_handler, mocker):
    date = datetime.datetime(2020, 1, 1, 10, 00, tzinfo=pytz.utc)
    mocker.patch.object(CacheHandler, '_get_expiration_time', return_value=int(date.timestamp()))

    cache_handler._save_cache_dynamo('321123')
    assert cache_handler._get_cache_from_dynamo() == '321123'
    assert cache_handler.max_age == 36000

    dynamodb.delete_item(
        TableName='tst-cache',
        Key={
            'key': {
                'S': 'fake_key'
            }
        }
    )

    assert cache_handler._get_cache_from_dynamo() is None


@freeze_time(datetime.datetime(2020, 1, 1, 00, 00, tzinfo=pytz.utc).isoformat())
def test_get_cache_max_age(cache_handler):
    date = datetime.datetime(2020, 1, 1, 23, 00, tzinfo=pytz.utc)
    cache_handler._get_cache_max_age(int(date.timestamp()))
    assert cache_handler.max_age == 82800
