def sugerir_divisao(disponibilidade_dias: int):
    if disponibilidade_dias >= 5:
        return "ABC 2x (Push/Pull/Legs)"
    elif disponibilidade_dias >= 3:
        return "ABC (Push/Pull/Legs)"
    return "Fullbody"

def calcular_progressao(carga_atual: float, reps_feitas: int, reps_alvo: int):
    if reps_feitas > reps_alvo:
        return round(carga_atual * 1.05, 1)
    return carga_atual

def validar_volume_seguro(series_por_musculo: int):
    if series_por_musculo > 24:
        return {"status": "perigoso", "aviso": "Volume excessivo! Risco de lesão."}
    return {"status": "seguro", "aviso": "Volume dentro dos padrões biomecânicos."}