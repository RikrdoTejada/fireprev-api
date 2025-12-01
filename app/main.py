from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.config import settings
from app.routers import lecturas, sensores, alertas
from app import models 

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(lecturas.router, prefix="/api/v1/lecturas", tags=["Lecturas"])
app.include_router(sensores.router, prefix="/api/v1/sensores", tags=["Sensores"])
app.include_router(alertas.router, prefix="/api/v1/alertas", tags=["Alertas"]) 

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Esto crea las tablas 'lecturas', 'alertas', 'sensores', etc. si no existen
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"mensaje": "API FirePrev Operativa"}