import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.calculator import calcular_tmb, calcular_macros

def test_calculo_tmb_homem():
    res = calcular_tmb(80, 180, 25, "m")
    assert res == 1805

def test_calculo_macros_bulking():
    tmb = 2000
    res = calcular_macros(tmb, "bulking")
    assert res["calorias_alvo"] == 2900
    assert res["proteina_g"] > 0 