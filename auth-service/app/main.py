from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TitanTrack AI - Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "sua_chave_ultra_secreta_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "guilherme" and form_data.password == "12345":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        data = {"sub": form_data.username, "exp": datetime.utcnow() + access_token_expires}
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")