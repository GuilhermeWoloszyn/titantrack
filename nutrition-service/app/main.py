from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.services.calculator import calcular_tmb, calcular_macros
from .database import get_nutrition_db

app = FastAPI(title="TitanTrack AI - Nutrition Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "sua_chave_ultra_secreta_aqui"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8002/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")

class UserData(BaseModel):
    peso: float
    altura: int
    idade: int
    sexo: str
    objetivo: str

@app.post("/calcular-dieta")
async def post_calcular_dieta(
    data: UserData, 
    user: str = Depends(get_current_user),
    db = Depends(get_nutrition_db)
):
    tmb = calcular_tmb(data.peso, data.altura, data.idade, data.sexo)
    plano_nutricional = calcular_macros(tmb, data.objetivo.lower())
    
    documento_dieta = {
        "usuario": user,
        "dados_entrada": data.dict(),
        "resultado": plano_nutricional,
        "data_criacao": datetime.utcnow()
    }

    try:
        await db.insert_one(documento_dieta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao persistir no MongoDB: {str(e)}")
    
    return {
        "usuario_logado": user,
        "plano": plano_nutricional,
        "status_banco": "Documento persistido no MongoDB"
    }

@app.get("/historico")
async def get_historico(db = Depends(get_nutrition_db)):
    cursor = db.find().sort("data_criacao", -1).limit(10)
    dietas = await cursor.to_list(length=10)
    
    for dieta in dietas:
        dieta["_id"] = str(dieta["_id"])
    
    return dietas