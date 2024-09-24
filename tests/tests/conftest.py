import pytest
from consult.pom.auth import get_access_token

@pytest.fixture
def auth_token():
    return get_access_token()