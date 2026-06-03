import os
import sys
from unittest.mock import Mock, patch

import httpx
from fastapi.testclient import TestClient

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200

    dados = response.json()

    assert dados["message"] == (
        "BFF Service operacional e conectado aos bancos"
    )

    assert "ambiente" in dados


def test_perfil_completo_sem_token():

    payload = {
        "usuario": "Guilherme",
        "treino": {},
        "dieta": {}
    }

    response = client.post(
        "/aluno/perfil-completo",
        json=payload
    )

    assert response.status_code == 401

    assert response.json()["detail"] == (
        "Token não fornecido"
    )


def test_historico_sem_token():

    response = client.get(
        "/aluno/historico-geral"
    )

    assert response.status_code == 401

    assert response.json()["detail"] == (
        "Token não fornecido"
    )


@patch("app.main.httpx.AsyncClient.post")
def test_login_sucesso(mock_post):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "access_token": "token123"
    }

    mock_post.return_value = mock_response

    response = client.post(
        "/auth/login",
        data={
            "username": "guilherme",
            "password": "12345"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "access_token": "token123"
    }


@patch("app.main.httpx.AsyncClient.post")
def test_login_erro(mock_post):

    mock_response = Mock()

    mock_response.status_code = 401

    mock_response.json.return_value = {
        "detail": "Unauthorized"
    }

    mock_post.return_value = mock_response

    response = client.post(
        "/auth/login",
        data={
            "username": "guilherme",
            "password": "errado"
        }
    )

    assert response.status_code == 401


@patch("app.main.httpx.AsyncClient.post")
def test_login_servico_indisponivel(mock_post):

    mock_post.side_effect = httpx.RequestError(
        "Serviço indisponível"
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "guilherme",
            "password": "12345"
        }
    )

    assert response.status_code == 503


@patch("app.main.httpx.AsyncClient.post")
def test_perfil_completo_sucesso(mock_post):

    dieta_response = Mock()

    dieta_response.status_code = 200

    dieta_response.json.return_value = {
        "calorias": 2500
    }

    treino_response = Mock()

    treino_response.status_code = 200

    treino_response.json.return_value = {
        "treino": "ABC"
    }

    mock_post.side_effect = [
        dieta_response,
        treino_response
    ]

    response = client.post(
        "/aluno/perfil-completo",
        headers={
            "Authorization": "Bearer token"
        },
        json={
            "usuario": "Guilherme",
            "treino": {},
            "dieta": {}
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["usuario_logado"] == "Guilherme"

    assert body["status"] == (
        "Processamento concluído"
    )


@patch("app.main.httpx.AsyncClient.get")
def test_historico_sucesso(mock_get):

    treino_response = Mock()

    treino_response.status_code = 200

    treino_response.json.return_value = [
        {"treino": "ABC"}
    ]

    dieta_response = Mock()

    dieta_response.status_code = 200

    dieta_response.json.return_value = [
        {"calorias": 2500}
    ]

    mock_get.side_effect = [
        treino_response,
        dieta_response
    ]

    response = client.get(
        "/aluno/historico-geral",
        headers={
            "Authorization": "Bearer token"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        "historico_treinos_relacional_postgres"
        in body
    )

    assert (
        "historico_dietas_documental_mongo"
        in body
    )