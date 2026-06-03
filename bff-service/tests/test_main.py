import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_perfil_completo_sem_token():
    payload = {
        "usuario": "Guilherme",
        "treino": {},
        "dieta": {}
    }

    response = client.post("/aluno/perfil-completo", json=payload)

    assert response.status_code == 401


def test_login_sucesso():
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"token": "abc"}

        return MockResponse()

    with patch("httpx.AsyncClient.post", new=mock_post):
        response = client.post(
            "/auth/login",
            data={"username": "guilherme", "password": "123"}
        )

        assert response.status_code == 200


def test_historico_sucesso():
    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return [{"mock": "data"}]

        return MockResponse()

    with patch("httpx.AsyncClient.get", new=mock_get):
        response = client.get(
            "/aluno/historico-geral",
            headers={"Authorization": "Bearer token"}
        )

        assert response.status_code == 200