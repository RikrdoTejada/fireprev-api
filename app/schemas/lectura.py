from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LecturaBase(BaseModel):
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    humo_ppm: Optional[float] = None
    bateria_voltaje: Optional[float] = None

class LecturaCreate(LecturaBase):
    sensor_id: int


class LecturaResponse(LecturaBase):
    tiempo: datetime
    sensor_id: int
    
    class Config:
        from_attributes = True

# Esquema para Alertas 
class AlertaResponse(BaseModel):
    id: int
    sensor_id: int
    mensaje: str
    nivel: str
    fecha: datetime
    atendida: bool

    class Config:
        from_attributes = True