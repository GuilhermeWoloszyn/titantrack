import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_main():
    response = client.get("/historico")
    assert response.status_code in [200, 401]


def calcular_progressao(carga_atual, fator=1.05):
    return round(carga_atual * fator, 1)

def test_calculo_progressao_carga():
    carga_inicial = 60.0
    carga_esperada = 63.0
    assert calcular_progressao(carga_inicial) == carga_esperada

def test_calculo_carga_pesada():
    assert calcular_progressao(100.0) == 105.0