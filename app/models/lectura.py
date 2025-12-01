from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Lectura(Base):
    """
    Modelo optimizado para TimescaleDB (Series Temporales).
    Almacena las mediciones de los sensores ESP32 (DHT22, MQ-2).
    """
    __tablename__ = "lecturas"

    # En TimescaleDB, la clave primaria DEBE incluir la columna de tiempo.
    # Usamos una clave compuesta (tiempo + sensor_id)
    tiempo = Column(DateTime(timezone=True), server_default=func.now(), primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensores.id"), primary_key=True, index=True)
    
    # Métricas ambientales 
    temperatura = Column(Float, nullable=True)  # Sensor DHT22
    humedad = Column(Float, nullable=True)      # Sensor DHT22
    humo_ppm = Column(Float, nullable=True)     # Sensor MQ-2 (Gases/Humo)
    
    # Nivel de batería para monitoreo de salud del nodo 
    bateria_voltaje = Column(Float, nullable=True) 

class Alerta(Base):
    """
    Tabla estándar para registrar eventos críticos.
    Se consulta cuando se detectan anomalías (Temp > 35°C, etc).
    """
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensores.id"))
    
    # Detalles de la alerta
    mensaje = Column(String)    # Ej: "Incendio detectado: Temp 45°C"
    nivel = Column(String)      # Ej: "CRITICO", "ADVERTENCIA"
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    
    # Gestión de incidencias
    atendida = Column(Boolean, default=False) # Para que el operador del COER marque visto