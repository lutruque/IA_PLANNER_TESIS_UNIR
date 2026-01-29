from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Agente IA Turístico",
    description="Generación de itinerarios turísticos con IA generativa",
    version="1.0"
)

app.include_router(router)
