import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)
