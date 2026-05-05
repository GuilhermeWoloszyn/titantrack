from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, get_current_user

client = TestClient(app)

def override_get_current_user():
    return "usuario_teste"

app.dependency_overrides[get_current_user] = override_get_current_user

def test_status_api():
    response = client.get("/")
    assert response.status_code in [200, 404]

def test_fluxo_dieta_com_seguranca_mockada():
    payload = {
        "peso": 80.0, "altura": 180, "idade": 25, "sexo": "m", "objetivo": "bulking"
    }
    response = client.post("/calcular-dieta", json=payload)
    assert response.status_code == 200