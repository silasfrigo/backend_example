import pytest

from prescriptions.crud.dependents import DependentsAPI


@pytest.fixture
def dependents():
    dependents = DependentsAPI()
    yield dependents
