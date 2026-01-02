# 🔥 FirePrev API — Sistema de Alerta Temprana de Incendios Forestales

**FirePrev** es una plataforma IoT para el monitoreo en tiempo real de variables ambientales en zonas forestales (temperatura, humedad y humo), con detección de anomalías y emisión de alertas tempranas para la prevención de incendios.

---

## 🎯 Objetivo
Detectar condiciones de riesgo de incendio mediante la recolección y análisis continuo de datos de sensores, visualizando métricas clave y activando alertas automáticas ante umbrales críticos.

---

## 🧱 Arquitectura del Sistema
Arquitectura contenerizada orientada a microservicios:

- **API Gateway (FastAPI):** Ingesta de datos IoT y gestión de Zonas, Gateways y Sensores.
- **Base de Datos:** PostgreSQL 14 con **TimescaleDB** para series temporales.
- **Visualización:** Grafana para dashboards en tiempo real, mapas y alertas.
- **Simulación IoT:** Script Python que emula sensores (patrones sinusoidales + escenarios de incendio).

---

## 📦 Stack Tecnológico
- **Backend:** Python 3.9+, FastAPI, SQLAlchemy, Pydantic
- **Base de Datos:** PostgreSQL 14 + TimescaleDB
- **Observabilidad:** Grafana
- **Infraestructura:** Docker & Docker Compose

---

## 📋 Requisitos Previos
- Docker Desktop (en ejecución)
- Git
- Python 3.9+ (solo para simulación local)

---

## 🚀 Instalación y Despliegue

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/RikrdoTejada/fireprev-api.git
cd fireprev-api
```

### 2️⃣ Configurar variables de entorno (SMTP)
Para habilitar notificaciones por correo desde Grafana, edita `docker-compose.yml`:

```yaml
GF_SMTP_ENABLED: "true"
GF_SMTP_USER: "tu_correo@gmail.com"
GF_SMTP_PASSWORD: "password_de_aplicacion"
GF_SMTP_FROM_ADDRESS: "FirePrev <tu_correo@gmail.com>"
```
> ⚠️ Recomendado usar **App Passwords** de Gmail, no tu contraseña personal.

---

### 3️⃣ Levantar los servicios
```bash
docker-compose up -d --build
```

---

### 4️⃣ Inicialización de TimescaleDB (solo la primera vez)
```bash
docker exec -it fireprev_db psql -U fireprev -d fireprev
```

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
SELECT create_hypertable('lecturas', 'tiempo', if_not_exists => TRUE);
\q
```

---

## 🔌 Uso del Sistema

### 📡 API REST
- Swagger UI: http://localhost:8000/docs
- Permite:
  - Crear zonas geográficas
  - Registrar sensores
  - Ingestar lecturas ambientales

---

### 📊 Grafana (Dashboards)
- URL: http://localhost:3000
- Credenciales por defecto:
  - **Usuario:** admin
  - **Password:** admin

**Dashboards incluidos:**
- Mapa geoespacial de zonas
- Temperatura vs Humedad
- Nivel de humo con alertas tipo semáforo
- Historial de eventos y alertas

---

## 🌲 Simulador IoT
Emula sensores LoRaWAN enviando datos periódicos a la API.

### 1️⃣ Preparar entorno
```bash
cd simulation
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Ejecutar simulación
```bash
python simulador.py
```

### 3️⃣ Escenarios disponibles
- **1:** Modo normal (ciclo día/noche)
- **2:** Incendio en zona sur
- **3:** Incendio en zona norte

---

## 📂 Estructura del Proyecto
```
fireprev-api/
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   └── services/
├── simulation/
│   ├── simulador.py
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🔐 Seguridad
- Acceso a Grafana mediante roles:
  - **admin:** Control total
  - **viewer:** Solo lectura
- Alertas automáticas por correo cuando el humo supera **200 ppm**

---

## 📡 Puertos
| Servicio     | Puerto | Descripción |
|-------------|--------|-------------|
| API         | 8000   | Backend FastAPI |
| Grafana     | 3000   | Dashboards |
| PostgreSQL  | 5433   | Base de datos |

---

## 🧭 Roadmap
- Autenticación JWT en API
- Integración con mapas satelitales
- Modelo ML para predicción temprana
- Soporte multi-organización

---

## 📄 Licencia
Proyecto académico / demostrativo. Uso libre para fines educativos.

