from pydantic import BaseModel
from typing import Optional

# --- Esquemas para Zonas (Norte, Centro, Sur) ---
class ZonaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class ZonaCreate(ZonaBase):
    pass

class ZonaResponse(ZonaBase):
    id: int
    class Config:
        from_attributes = True

# --- Esquemas para Sensores ---
class SensorBase(BaseModel):
    codigo: str       # Ej: "SEN-T01"
    modelo: str       # Ej: "ESP32-DHT22"
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    activo: bool = True

class SensorCreate(SensorBase):
    zona_id: int

class SensorResponse(SensorBase):
    id: int
    zona_id: int
    class Config:
        from_attributes = True