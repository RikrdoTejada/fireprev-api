import requests
import time
import random
import sys
import math
from datetime import datetime

# --- CONFIGURACIÓN ---
API_URL = "http://localhost:8000/api/v1"
FRECUENCIA_ENVIO = 5  

ZONAS_CONFIG = [
    { "id": 1, "nombre": "Zona Norte", "descripcion": "Cobertura forestal", "lat": -10.4222, "lon": -75.5256 },
    { "id": 2, "nombre": "Zona Centro", "descripcion": "Área urbana", "lat": -10.4261, "lon": -75.5187 },
    { "id": 3, "nombre": "Zona Sur", "descripcion": "Bosques primarios", "lat": -10.4327, "lon": -75.5232 }
]

SENSORES_POR_ZONA = 5
SENSORES_DB = {"Norte": [], "Centro": [], "Sur": []}

# Cada sensor tendrá su propio "reloj interno" para que las ondas no sean idénticas
# Formato: { sensor_id: { 't': 0, 'fase': random_float, 'base_temp': 22.0 } }
ESTADO_SENSORES = {}

def generar_coordenada_cercana(lat_centro, lon_centro, radio_metros=50):
    delta_lat = (random.uniform(-1, 1) * radio_metros) / 111320
    delta_lon = (random.uniform(-1, 1) * radio_metros) / (40075000 * math.cos(math.radians(lat_centro)) / 360)
    return lat_centro + delta_lat, lon_centro + delta_lon

def inicializar_infraestructura():
    print("🏗️  Sincronizando infraestructura...")
    for zona in ZONAS_CONFIG:
        try:
            requests.post(f"{API_URL}/sensores/zonas/", json={
                "nombre": zona["nombre"], "descripcion": zona["descripcion"],
                "latitud": zona["lat"], "longitud": zona["lon"]
            })
        except: pass

    try:
        response = requests.get(f"{API_URL}/sensores/?limit=1000")
        existentes = response.json()
    except: return

    for zona in ZONAS_CONFIG:
        clave = zona['nombre'].replace("Zona ", "")
        en_zona = [s['id'] for s in existentes if s['zona_id'] == zona['id']]
        
        if en_zona:
            SENSORES_DB[clave] = en_zona
        else:
            print(f"⚠️ Creando sensores para {zona['nombre']}...")
            for i in range(1, SENSORES_POR_ZONA + 1):
                lat, lon = generar_coordenada_cercana(zona['lat'], zona['lon'])
                payload = {
                    "codigo": f"SEN-{clave.upper()}-{i:03d}",
                    "modelo": "ESP32-LoRa", "zona_id": zona['id'],
                    "latitud": lat, "longitud": lon, "activo": True
                }
                r = requests.post(f"{API_URL}/sensores/", json=payload)
                if r.status_code == 200: SENSORES_DB[clave].append(r.json()['id'])

def calcular_valores_ondulatorios(sensor_id, escenario="normal"):
    """
    Usa funciones SENO para generar curvas naturales y suaves.
    """
    # Inicializar sensor si es nuevo
    if sensor_id not in ESTADO_SENSORES:
        ESTADO_SENSORES[sensor_id] = {
            't': random.randint(0, 100),  # Tiempo inicial aleatorio
            'fase': random.uniform(0, 2 * math.pi), # Desfase para que no vayan todos igual
            'velocidad': random.uniform(0.05, 0.1), # Qué tan rápido cambia el clima
            'volt': random.uniform(4.0, 4.2)
        }
    
    estado = ESTADO_SENSORES[sensor_id]
    
    # Avanzar el tiempo
    estado['t'] += estado['velocidad']
    
    # --- ESCENARIO NORMAL (Curvas Suaves) ---
    # Fórmula: Temperatura Base + Amplitud * Seno(tiempo + fase)
    # Esto crea una onda suave que sube y baja entre 20°C y 26°C
    temp_base = 23.0
    temp = temp_base + 3.0 * math.sin(estado['t'] + estado['fase'])
    
    # Agregamos un micro-ruido muy pequeño (0.1) para que no sea una línea matemática perfecta
    temp += random.uniform(-0.1, 0.1)

    # La humedad es INVERSA a la temperatura (Ley física básica)
    # Si sube temp, baja humedad.
    humedad = 100 - (temp * 2.5) # Fórmula simple de correlación inversa
    humedad += random.uniform(-1.0, 1.0) # Un poco de variación
    
    humo = 0.0
    
    # Simulación de batería (baja muy lento)
    estado['volt'] -= 0.0001
    if estado['volt'] < 3.3: estado['volt'] = 4.2

    # --- SOBRESCRIBIR SI HAY INCENDIO ---
    if escenario == "incendio":
        # Rompemos la curva suave y forzamos subida exponencial
        temp = 45.0 + (random.uniform(0, 5))
        humedad = 15.0 + (random.uniform(-2, 2))
        humo = 350.0 + (random.uniform(-50, 50))
        
    elif escenario == "calor":
        temp += 10.0 # Ola de calor: Sumamos 10 grados a la curva normal
        humedad -= 20.0
        humo = random.uniform(0, 5)

    # Clamping (Límites lógicos)
    temp = max(0, min(100, temp))
    humedad = max(0, min(100, humedad))

    return {
        "sensor_id": sensor_id,
        "temperatura": round(temp, 2),
        "humedad": round(humedad, 2),
        "humo_ppm": round(humo, 2),
        "bateria_voltaje": round(estado['volt'], 3)
    }

def enviar_telemetria(zona_nombre, escenario):
    if not SENSORES_DB[zona_nombre]: return

    # Elegir SOLO UN sensor aleatorio por ciclo para enviar datos
    # O enviar todos con pausa. La mejor opción visual es enviar TODOS con pausa.
    
    for sensor_id in SENSORES_DB[zona_nombre]:
        data = calcular_valores_ondulatorios(sensor_id, escenario)
        try:
            requests.post(f"{API_URL}/lecturas/", json=data)
        except: pass
        
        # --- PAUSA CLAVE ---
        # Si tienes 5 sensores y envías cada 30s, espera un poco entre cada uno
        # para que no lleguen al mismo milisegundo a la base de datos.
        time.sleep(0.01) 
    
    print(f"📡 {zona_nombre}: Telemetría enviada ({escenario})")

def main():
    print(f"--- 🌲 SIMULADOR DE CLIMA REALISTA ({FRECUENCIA_ENVIO}s) 🌲 ---")
    inicializar_infraestructura()
    
    print("\n1. Modo Normal (Ciclos naturales)")
    print("2. 🔥 INCENDIO en SUR")
    print("3. 🔥 INCENDIO en NORTE")
    opcion = input("Elige escenario: ")

    try:
        while True:
            esc_sur = "incendio" if opcion == "2" else "normal"
            esc_norte = "incendio" if opcion == "3" else "normal"
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Generando ondas climáticas...")
            enviar_telemetria("Norte", esc_norte)
            enviar_telemetria("Centro", "normal")
            enviar_telemetria("Sur", esc_sur)
            
            time.sleep(FRECUENCIA_ENVIO)
            
    except KeyboardInterrupt:
        print("\nApagando simulador.")

if __name__ == "__main__":
    main()