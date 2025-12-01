from sqlalchemy.ext.asyncio import AsyncSession
from app.models import lectura as lectura_models

async def analizar_riesgo(db: AsyncSession, lectura: lectura_models.Lectura):
    """
    Reglas de negocio para detectar condiciones de riesgo basadas en las lecturas de los sensores.:
    - Temp > 30°C (Critico)
    - Humedad < 30% (Riesgo)
    - Humo > 200 ppm (Incendio activo)
    """
    
    nivel_alerta = None
    mensaje = ""

    # Regla 1: Detección de Fuego/Humo
    if lectura.humo_ppm and lectura.humo_ppm > 200:
        nivel_alerta = "CRITICO"
        mensaje = f"HUMO DETECTADO: {lectura.humo_ppm} ppm"

    # Regla 2: Condiciones extremas (Triángulo del fuego)
    elif (lectura.temperatura and lectura.temperatura > 35.0) and \
         (lectura.humedad and lectura.humedad < 30.0):
        nivel_alerta = "ALTO"
        mensaje = f"Condiciones de ignición: T {lectura.temperatura}°C / H {lectura.humedad}%"

    # Si hay alerta, la guardamos
    if nivel_alerta:
        nueva_alerta = lectura_models.Alerta(
            sensor_id=lectura.sensor_id,
            mensaje=mensaje,
            nivel=nivel_alerta
        )
        db.add(nueva_alerta)
        print(f"⚠️ ALERTA GENERADA: {mensaje}")