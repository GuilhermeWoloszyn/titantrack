from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.services.trainer import sugerir_divisao, calcular_progressao, validar_volume_seguro
from .database import engine, Base, get_db
from .models import TreinoSalvo

app = FastAPI(title="TitanTrack AI - Workout Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class WorkoutRequest(BaseModel):
    usuario: str = "Guilherme"
    exercicio: str
    carga_atual: float
    dias_disponiveis: int = 3   
    reps_feitas: int = 10       
    reps_alvo: int = 10        
    series_semanais: int = 12   

@app.post("/gerar-treino")
async def post_gerar_treino(data: WorkoutRequest, db: AsyncSession = Depends(get_db)):
    divisao = sugerir_divisao(data.dias_disponiveis)
    nova_carga = calcular_progressao(data.carga_atual, data.reps_feitas, data.reps_alvo)
    seguranca = validar_volume_seguro(data.series_semanais)
    
    try:
        novo_registro = TreinoSalvo(
            usuario="Guilherme", 
            exercicio="Supino Reto",
            carga_calculada=nova_carga
        )
        db.add(novo_registro)
        await db.commit() 
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")
    
    return {
        "divisao_sugerida": divisao,
        "proxima_carga": nova_carga,
        "analise_seguranca": seguranca,
        "status_banco": "Dados persistidos no PostgreSQL"
    }

@app.get("/historico")
async def get_historico(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TreinoSalvo).order_by(TreinoSalvo.data_criacao.desc()))
    treinos = result.scalars().all()
    return treinos