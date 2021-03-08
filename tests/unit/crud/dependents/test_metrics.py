import pytest

from fastapi import HTTPException
from requests import Session
from requests.exceptions import ConnectionError

from tests.fixtures import dependent_metrics, metrics


def test_send_metrics_api(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 201
    fake_request.json_return = dependent_metrics
    mocker.patch.object(Session, 'post', return_value=fake_request)

    assert dependents.send_metrics(metrics) is True


def test_send_metrics_api_404(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 400
    mocker.patch.object(Session, 'post', return_value=fake_request)

    with pytest.raises(HTTPException):
        dependents.send_metrics(metrics)


def test_send_metrics_api_conn_error(dependents, mocker, dynamodb, fake_request):
    fake_request.status_code_return = 500
    mocker.patch.object(Session, 'post', side_effect=ConnectionError())

    with pytest.raises(HTTPException):
        dependents.send_metrics(metrics)
