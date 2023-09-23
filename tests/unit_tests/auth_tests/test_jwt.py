import pytest
from src.auth.auth import JwtManager
from src.auth.exceptions import JwtNotValidError, JWTExpiredError
from datetime import datetime, timedelta


# Parameterized sample data
@pytest.fixture(params=["test_user1", "test_user2", "test_user3"])
def sample_data(request):
    return request.param


# Unit tests for JwtManager class
class TestJwtManagerUnit:
    def test_get_expire_time(self):
        expire_time = JwtManager._get_expire_time(10)
        assert isinstance(expire_time, datetime)

    def test_get_token_pattern(self):
        token_pattern = JwtManager._get_token_pattern()
        assert isinstance(token_pattern, dict)

    def test_is_token_expired(self):
        timestamp = datetime.utcnow().timestamp() - 3600
        payload = {"exp": timestamp}
        assert JwtManager._is_token_expired(payload) is True

    def test_create_token(self, sample_data):
        encoded_token = JwtManager.create_token(sample_data)
        assert isinstance(encoded_token, str)

    # TODO: move to integration tests
    def test_read_token_valid(self, sample_data):
        encoded_token = JwtManager.create_token(sample_data)
        payload = JwtManager.read_token(encoded_token)
        assert payload["sub"] == sample_data

    def test_read_token_invalid(self):
        with pytest.raises(JwtNotValidError):
            JwtManager.read_token("invalid_token")
