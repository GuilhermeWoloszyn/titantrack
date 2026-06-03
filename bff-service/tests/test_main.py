import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import httpx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "BFF Service operacional e conectado aos bancos"
    assert "ambiente" in response.json()

def test_perfil_completo_sem_token():
    payload = {
        "usuario": "Guilherme",
        "treino": {},
        "dieta": {}
    }

    response = client.post("/aluno/perfil-completo", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Token não fornecido"

def test_perfil_completo_sucesso():
    class MockResponse:
        status_code = 200

        def json(self):
            return {"ok": True}

    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, *args, **kwargs):
            return MockResponse()

    with patch("httpx.AsyncClient", return_value=MockClient()):
        response = client.post(
            "/aluno/perfil-completo",
            json={
                "usuario": "Guilherme",
                "treino": {},
                "dieta": {}
            },
            headers={"Authorization": "Bearer token"}
        )

        assert response.status_code == 200
        assert "dados_nutricionais" in response.json()
        assert "plano_treino" in response.json()

def test_login_sucesso():
    class MockResponse:
        status_code = 200

        def json(self):
            return {"token": "abc"}

    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, *args, **kwargs):
            return MockResponse()

    with patch("httpx.AsyncClient", return_value=MockClient()):
        response = client.post(
            "/auth/login",
            data={"username": "guilherme", "password": "123"}
        )

        assert response.status_code == 200
        assert response.json()["token"] == "abc"

def test_login_erro_status():
    class MockResponse:
        status_code = 401

        def json(self):
            return {"detail": "invalid"}

    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, *args, **kwargs):
            return MockResponse()

    with patch("httpx.AsyncClient", return_value=MockClient()):
        response = client.post(
            "/auth/login",
            data={"username": "x", "password": "y"}
        )

        assert response.status_code == 401

def test_login_exception():
    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, *args, **kwargs):
            raise httpx.RequestError("erro")

    with patch("httpx.AsyncClient", return_value=MockClient()):
        response = client.post(
            "/auth/login",
            data={"username": "x", "password": "y"}
        )

        assert response.status_code == 503

def test_historico_sucesso():
    class MockResponse:
        status_code = 200

        def json(self):
            return [{"mock": "data"}]

    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, *args, **kwargs):
            return MockResponse()

    with patch("httpx.AsyncClient", return_value=MockClient()):
        response = client.get(
            "/aluno/historico-geral",
            headers={"Authorization": "Bearer token"}
        )

        assert response.status_code == 200

def test_historico_exception():
    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, *args, **kwargs):
            raise Exception("erro geral")

    with patch("httpx.AsyncClient", return_value=MockClient()):
        response = client.get(
            "/aluno/historico-geral",
            headers={"Authorization": "Bearer token"}
        )

        assert response.status_code == 503