import requests
import time
import random
import sys
import math
from datetime import datetime

# --- CONFIGURACIÓN ---
API_URL = "http://localhost:8000/api/v1"
ZONAS_CONFIG = [
    {
        "id": 1, 
        "nombre": "Zona Norte", 
        "descripcion": "Cobertura forestal sector norte",
        "lat": -10.4222, "lon": -75.5256
    },
    {
        "id": 2, 
        "nombre": "Zona Centro", 
        "descripcion": "Área urbana y transición",
        "lat": -10.4261, "lon": -75.5187
    },
    {
        "id": 3, 
        "nombre": "Zona Sur", 
        "descripcion": "Bosques primarios y reserva",
        "lat": -10.4327, "lon": -75.5232
    }
]

# Cantidad de sensores a crear por zona si está vacía
SENSORES_POR_ZONA = 5 
FRECUENCIA_ENVIO = 5  # Segundos entre lecturas (Modificado)

# Diccionario para guardar los IDs de sensores detectados/creados
SENSORES_DB = {"Norte": [], "Centro": [], "Sur": []}

def generar_coordenada_cercana(lat_centro, lon_centro, radio_metros=50):
    delta_lat = (random.uniform(-1, 1) * radio_metros) / 111320
    delta_lon = (random.uniform(-1, 1) * radio_metros) / (40075000 * math.cos(math.radians(lat_centro)) / 360)
    return lat_centro + delta_lat, lon_centro + delta_lon

def inicializar_infraestructura():
    print(" Verificando infraestructura en la API...")
    
    # 1. Crear Zonas
    for zona in ZONAS_CONFIG:
        try:
            payload = {"nombre": zona["nombre"], "descripcion": zona["descripcion"]}
            requests.post(f"{API_URL}/sensores/zonas/", json=payload)
        except Exception:
            pass

    # 2. Verificar y Crear Sensores
    try:
        response = requests.get(f"{API_URL}/sensores/?limit=1000")
        sensores_existentes = response.json()
    except Exception as e:
        print(f"Error fatal conectando a la API: {e}")
        sys.exit(1)

    for zona in ZONAS_CONFIG:
        sensores_en_zona = [s for s in sensores_existentes if s['zona_id'] == zona['id']]
        clave = zona['nombre'].replace("Zona ", "")
        
        if len(sensores_en_zona) > 0:
            print(f"{zona['nombre']}: Encontrados {len(sensores_en_zona)} sensores existentes.")
            SENSORES_DB[clave] = [s['id'] for s in sensores_en_zona]
        else:
            print(f"{zona['nombre']}: Vacía. Creando {SENSORES_POR_ZONA} sensores...")
            for i in range(1, SENSORES_POR_ZONA + 1):
                lat, lon = generar_coordenada_cercana(zona['lat'], zona['lon'])
                codigo = f"SEN-{clave.upper()}-{i:03d}"
                
                payload = {
                    "codigo": codigo, "modelo": "ESP32-LoRa", "zona_id": zona['id'],
                    "latitud": lat, "longitud": lon, "activo": True
                }
                
                resp = requests.post(f"{API_URL}/sensores/", json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    SENSORES_DB[clave].append(data['id'])
                    print(f" Creado: {codigo}")

def generar_lectura(zona_nombre, escenario="normal"):
    # Valores Base
    temp = random.uniform(20.0, 26.0)
    humedad = random.uniform(50.0, 70.0)
    humo = 0.0
    voltaje = random.uniform(3.8, 4.2)

    # Escenarios
    if escenario == "incendio":
        temp = random.uniform(45.0, 60.0)
        humedad = random.uniform(10.0, 20.0)
        humo = random.uniform(300.0, 500.0)
        voltaje = random.uniform(3.5, 3.8)
    elif escenario == "calor":
        temp = random.uniform(32.0, 38.0)
        humedad = random.uniform(25.0, 35.0)
        humo = random.uniform(0.0, 10.0)

    if not SENSORES_DB[zona_nombre]: return None
    sensor_id = random.choice(SENSORES_DB[zona_nombre])

    return {
        "sensor_id": sensor_id,
        "temperatura": round(temp, 2),
        "humedad": round(humedad, 2),
        "humo_ppm": round(humo, 2),
        "bateria_voltaje": round(voltaje, 2)
    }

def enviar_datos(zona_nombre, escenario):
    data = generar_lectura(zona_nombre, escenario)
    if not data: return

    try:
        requests.post(f"{API_URL}/lecturas/", json=data)
        # Solo imprimimos un log corto para no saturar la consola
        hora = datetime.now().strftime("%H:%M:%S")
        estado = "*" if escenario == "incendio" else "-"
        print(f"[{hora}] {estado} {zona_nombre}: ID {data['sensor_id']} enviado.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("---  SIMULADOR IOT (Frecuencia: 60s) ---")
    inicializar_infraestructura()
    print("-" * 50)
    
    print("1. Modo Tranquilo (Todo Normal)")
    print("2.  INCENDIO en ZONA SUR")
    print("3.  INCENDIO en ZONA NORTE")
    print("4.  OLA DE CALOR en ZONA CENTRO")
    
    opcion = input("\nSelecciona un escenario (1-4): ")
    
    try:
        print(f"\n Iniciando envío de datos cada {FRECUENCIA_ENVIO} segundos...")
        while True:
            escenario_sur = "incendio" if opcion == "2" else "normal"
            escenario_norte = "incendio" if opcion == "3" else "normal"
            escenario_centro = "calor" if opcion == "4" else "normal"

            # Enviar datos
            enviar_datos("Norte", escenario_norte)
            enviar_datos("Centro", escenario_centro)
            enviar_datos("Sur", escenario_sur)

            print(f"💤 Esperando {FRECUENCIA_ENVIO}s para el siguiente ciclo...")
            time.sleep(FRECUENCIA_ENVIO) 
            
    except KeyboardInterrupt:
        print("\n Simulador detenido.")

if __name__ == "__main__":
    main()