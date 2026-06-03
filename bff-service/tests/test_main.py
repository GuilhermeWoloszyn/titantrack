import os
import sys
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

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
    assert response.json()["detail"] == "Token não fornecido"


@patch("app.main.httpx.AsyncClient.post")
def test_login_sucesso(mock_post):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"token": "abc"}

    mock_post.return_value = mock_response

    response = client.post(
        "/auth/login",
        data={"username": "guilherme", "password": "123"}
    )

    assert response.status_code == 200


@patch("app.main.httpx.AsyncClient.post")
def test_login_erro(mock_post):

    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {"detail": "Unauthorized"}

    mock_post.return_value = mock_response

    response = client.post(
        "/auth/login",
        data={"username": "guilherme", "password": "errado"}
    )

    assert response.status_code == 401


@patch("app.main.httpx.AsyncClient.get")
def test_historico(mock_get):

    mock_workout = Mock()
    mock_workout.status_code = 200
    mock_workout.json.return_value = [{"treino": "A"}]

    mock_nutrition = Mock()
    mock_nutrition.status_code = 200
    mock_nutrition.json.return_value = [{"calorias": 2000}]

    mock_get.side_effect = [mock_workout, mock_nutrition]

    response = client.get(
        "/aluno/historico-geral",
        headers={"Authorization": "Bearer token"}
    )

    assert response.status_code == 200
    assert "historico_treinos_relacional_postgres" in response.json()