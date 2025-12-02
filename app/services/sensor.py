from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import sensor as sensor_models
from app.schemas import sensor as sensor_schemas

async def get_zona_by_nombre(db: AsyncSession, nombre: str):
    result = await db.execute(select(sensor_models.Zona).where(sensor_models.Zona.nombre == nombre))
    return result.scalars().first()

async def create_zona(db: AsyncSession, zona: sensor_schemas.ZonaCreate):
    db_zona = sensor_models.Zona(**zona.model_dump())
    db.add(db_zona)
    await db.commit()
    await db.refresh(db_zona)
    return db_zona

async def get_sensor_by_codigo(db: AsyncSession, codigo: str):
    result = await db.execute(select(sensor_models.Sensor).where(sensor_models.Sensor.codigo == codigo))
    return result.scalars().first()

async def create_sensor(db: AsyncSession, sensor: sensor_schemas.SensorCreate):
    db_sensor = sensor_models.Sensor(**sensor.model_dump())
    db.add(db_sensor)
    await db.commit()
    await db.refresh(db_sensor)
    return db_sensor

async def get_sensores(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(sensor_models.Sensor).offset(skip).limit(limit))
    return result.scalars().all()