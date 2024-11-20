import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Тестовый клиент FastAPI"""
    return TestClient(app)


@pytest.fixture
def mock_db(mocker):
    return mocker.patch(
        "models.model_settings.db_helper.scoped_session_dependency", new=AsyncMock()
    )


@pytest.fixture
def mock_redis(mocker):
    mock_redis_instance = AsyncMock()
    mocker.patch("models.model_settings.get_redis", return_value=mock_redis_instance)
    return mock_redis_instance
