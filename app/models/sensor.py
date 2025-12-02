from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Zona(Base):
    __tablename__ = "zonas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)

class Sensor(Base):
    __tablename__ = "sensores"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True) # Ej: SEN-Norte-01
    
    # Relación con Zona
    zona_id = Column(Integer, ForeignKey("zonas.id"))
    
    modelo = Column(String)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    activo = Column(Boolean, default=True)