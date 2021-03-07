import pytest

from cache import file_cache
from fastapi.testclient import TestClient
from prescriptions.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope='function', autouse=True)
def clean_cache_auth():
    file_cache.clear()
