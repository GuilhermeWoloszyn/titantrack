def calcular_tmb(peso: float, altura: int, idade: int, sexo: str) -> float:
    if sexo.lower() == "m":
        return (10 * peso) + (6.25 * altura) - (5 * idade) + 5
    return (10 * peso) + (6.25 * altura) - (5 * idade) - 161

def calcular_macros(tmb: float, objetivo: str):
    multiplicador = 1.2
    calorias_manutencao = tmb * multiplicador
    
    if objetivo == "bulking":
        total_calorias = calorias_manutencao + 500
    elif objetivo == "cutting":
        total_calorias = calorias_manutencao - 500
    else:
        total_calorias = calorias_manutencao

    return {
        "calorias_alvo": round(total_calorias, 2),
        "proteina_g": round((total_calorias * 0.30) / 4, 2),
        "carboidrato_g": round((total_calorias * 0.50) / 4, 2),
        "gordura_g": round((total_calorias * 0.20) / 9, 2)
    }