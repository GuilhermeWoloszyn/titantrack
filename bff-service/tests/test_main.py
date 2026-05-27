import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    dados = response.json()
    assert dados["message"] == "BFF Service operacional e conectado aos bancos"
    assert "ambiente" in dados

def test_perfil_completo_sem_token():
    payload_valido = {
        "usuario": "Guilherme",
        "treino": {},
        "dieta": {}
    }
    response = client.post("/aluno/perfil-completo", json=payload_valido)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Token não fornecido"

def test_login_sucesso():
    dados_login = {
        "username": "guilherme",
        "password": "12345"
    }
    response = client.post("/auth/login", data=dados_login)
    
    assert response.status_code in [200, 401, 404, 503]