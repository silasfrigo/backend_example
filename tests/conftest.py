import pytest

from fastapi.testclient import TestClient
from prescriptions.lambda_handler import app


@pytest.fixture
def client():
    return TestClient(app)
