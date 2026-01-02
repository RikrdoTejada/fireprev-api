# 🔥 FirePrev API: Sistema de Alerta Temprana de Incendios Forestales

**FirePrev** es una solución IoT integral diseñada para el monitoreo en tiempo real de condiciones ambientales en zonas forestales. El sistema recolecta, procesa y visualiza datos de sensores (Temperatura, Humedad, Humo) para detectar anomalías y emitir alertas tempranas de incendios.

## 🚀 Arquitectura del Sistema

El proyecto utiliza una arquitectura de microservicios contenerizada:

* **API Gateway:** Desarrollada en **Python (FastAPI)**. Gestiona la ingesta de datos y la gestión de la infraestructura (Sensores/Zonas).
* **Base de Datos:** **PostgreSQL 14** optimizada con la extensión **TimescaleDB** para el manejo eficiente de series temporales (Time-Series Data).
* **Visualización:** **Grafana** conectado nativamente a la base de datos para dashboards en tiempo real y mapas geoespaciales.
* **Simulación:** Script en Python que genera datos climáticos realistas usando algoritmos sinusoidales y simulación de escenarios de incendio.

## 📋 Requisitos Previos

* [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y corriendo.
* [Git](https://git-scm.com/).
* Python 3.9+ (solo para ejecutar el simulador localmente).

## 🛠️ Instalación y Despliegue

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/RikrdoTejada/fireprev-api.git](https://github.com/RikrdoTejada/fireprev-api.git)
cd fireprev-api
```
### 2. Configurar Variables de Entorno
El proyecto ya incluye configuración por defecto en docker-compose.yml, pero para el envío de correos debes configurar tus credenciales SMTP.
Edita la sección environment del servicio grafana en docker-compose.yml:
```yaml
- GF_SMTP_ENABLED=true
- GF_SMTP_USER=tu_correo@gmail.com
- GF_SMTP_PASSWORD=tu_password_de_aplicacion
```
### 3. Levantar los Servicios (Docker)
Construye e inicia los contenedores:
```bash
docker-compose up -d --build
```
### 4. Inicialización de la Base de Datos (Primera Vez)
Es necesario activar la extensión de TimescaleDB y crear la hipertabla.
```bash
docker exec -it fireprev_db psql -U fireprev -d fireprev
```
Dentro de la consola SQL, pega:
```sql
-- Activar extensión Time-Series
CREATE EXTENSION IF NOT EXISTS timescaledb;
-- Convertir tabla estándar a Hipertabla particionada por tiempo
SELECT create_hypertable('lecturas', 'tiempo');
\q
```

## 💻 Uso del Sistema
### 📡 API Rest (Backend)
* Documentación Interactiva (Swagger UI): Accede a http://localhost:8000/docs
* Desde aquí puedes crear Zonas y registrar nuevos Sensores manualmente.

### 📊 Dashboard de Monitoreo (Grafana)
URL: http://localhost:3000

- Credenciales por defecto: admin / admin
- Paneles Incluidos:
  - Mapa Geoespacial de Zonas.
  - Gráficos de Temperatura vs Humedad (Correlación Inversa).
  - Nivel de Humo con Alertas de Semáforo.
  - Historial de Alertas.

### 🌲 Ejecutar el Simulador IoT
El simulador genera tráfico de datos realista emulando sensores LoRaWAN.
#### 1. Preparar entorno (Windows/Linux):
```bash
cd simulation
python -m venv venv
# Activar: .\venv\Scripts\activate (Windows) o source venv/bin/activate (Linux)
pip install requests
```
#### 2. Correr simulación:
```bash
python simulador.py
```
#### 3. Escenarios Disponibles:

* 1: Modo Normal (Ciclos climáticos naturales día/noche).
* 2: Incendio en Zona Sur (Aumento exponencial de T° y Humo).
* 3: Incendio en Zona Norte.

## 📂 Estructura del Proyecto
```
fireprev-api/
├── app/
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── models/              # Modelos SQLAlchemy (Tablas)
│   ├── schemas/             # Esquemas Pydantic (Validación)
│   ├── routers/             # Endpoints (Zonas, Sensores, Lecturas)
│   └── services/            # Lógica de negocio
├── simulation/
│   └── simulador.py         # Generador de datos IoT (Seno/Coseno)
├── docker-compose.yml       # Orquestación de contenedores
├── Dockerfile               # Construcción de la imagen de API
└── README.md                # Documentación
```
## ⚙️ Puertos
```
Servicio,Puerto Host,Descripción
API,8000,Backend FastAPI
Grafana,3000,Dashboards
PostgreSQL,5433,Base de datos (Puerto modificado para evitar conflictos locales)
```
## 🛡️ Seguridad y Accesos
- Roles en Grafana:
  - admin: Control total.
  - operador: Usuario de solo lectura (Viewer) para monitoreo en centros de control.
  - Alertas: Configurado vía SMTP (Gmail) para notificaciones críticas cuando el humo supera 200ppm.
