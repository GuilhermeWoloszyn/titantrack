from fastapi import FastAPI, Header, HTTPException, Form
from pydantic import BaseModel
import httpx

app = FastAPI(title="TitanTrack AI - BFF Service")

AUTH_SERVICE_URL = "http://auth-service:8000"
NUTRITION_SERVICE_URL = "http://nutrition-service:8000"
WORKOUT_SERVICE_URL = "http://workout-service:8000"

class PerfilPayload(BaseModel):
    usuario: str
    treino: dict
    dieta: dict

@app.get("/")
async def root():
    return {"message": "BFF Service operacional e conectado aos bancos"}

@app.post("/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/login",
                data={"username": username, "password": password}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.json())
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Serviço de Autenticação indisponível")

@app.post("/aluno/perfil-completo")
async def post_perfil_completo(payload: PerfilPayload, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")

    async with httpx.AsyncClient() as client:
        try:
            res_dieta = await client.post(
                f"{NUTRITION_SERVICE_URL}/calcular-dieta",
                headers={"Authorization": authorization},
                json=payload.dieta
            )
            
            res_treino = await client.post(
                f"{WORKOUT_SERVICE_URL}/gerar-treino",
                json=payload.treino
            )   

            return {
                "usuario_logado": payload.usuario,
                "dados_nutricionais": res_dieta.json() if res_dieta.status_code == 200 else res_dieta.json(),
                "plano_treino": res_treino.json() if res_treino.status_code == 200 else res_treino.json(),
                "status": "Processamento concluído"
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Erro de integração: {str(e)}")

@app.get("/aluno/historico-geral")
async def get_historico_geral(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")

    async with httpx.AsyncClient() as client:
        try:
            res_workout = await client.get(
                f"{WORKOUT_SERVICE_URL}/historico",
                headers={"Authorization": authorization}
            )

            res_nutrition = await client.get(
                f"{NUTRITION_SERVICE_URL}/historico",
                headers={"Authorization": authorization}
            )

            return {
                "usuario": "Guilherme",
                "historico_treinos_relacional_postgres": res_workout.json() if res_workout.status_code == 200 else [],
                "historico_dietas_documental_mongo": res_nutrition.json() if res_nutrition.status_code == 200 else [],
                "infraestrutura": "Dados agregados"
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Erro ao consolidar histórico: {str(e)}")