from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas import lectura as lectura_schemas 
from app.services import alerta as alerta_service

router = APIRouter()

@router.get("/", response_model=List[lectura_schemas.AlertaResponse])
async def listar_alertas(
    skip: int = 0, 
    limit: int = 50, 
    solo_activas: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene lista de alertas detectadas.
    Usa 'solo_activas=true' para ver solo las que no han sido atendidas.
    """
    return await alerta_service.get_alertas(
        db, 
        skip=skip, 
        limit=limit, 
        solo_no_atendidas=solo_activas
    )