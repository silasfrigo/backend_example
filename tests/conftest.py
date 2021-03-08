import boto3
import pytest

from fastapi.testclient import TestClient
from moto import mock_dynamodb2

from cache import file_cache
from prescriptions.main import app
from tests.fixtures import FakeRequest


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope='function', autouse=True)
def clean_cache_auth():
    file_cache.clear()


@pytest.fixture()
def dynamodb():
    with mock_dynamodb2():
        conn = boto3.client("dynamodb")
        conn.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'key',
                    'AttributeType': 'S'
                },
            ],
            TableName='tst-cache',
            KeySchema=[
                {
                    'AttributeName': 'key',
                    'KeyType': 'HASH'
                },
            ],
        )

        yield conn


@pytest.fixture
def fake_request():
    yield FakeRequest()
