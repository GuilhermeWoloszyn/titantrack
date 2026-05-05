from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class TreinoSalvo(Base):
    __tablename__ = "treinos"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String)
    exercicio = Column(String, default="Supino Reto") # Exemplo fixo para o trabalho
    carga_calculada = Column(Float)
    data_criacao = Column(DateTime, default=datetime.utcnow)