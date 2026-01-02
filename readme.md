# FirePrev API - Sistema de Detección Temprana de Incendios Forestales
## API REST desarrollada con **FastAPI** para la ingesta, procesamiento y monitoreo de datos provenientes de una red de sensores IoT (LoRaWAN) desplegada en el distrito de Huancabamba, Oxapampa.

Este proyecto forma parte de la **Capa de Aplicación** de la arquitectura de monitoreo ambiental.

## Características

* **Alto Rendimiento:** Procesamiento asíncrono para manejar miles de lecturas de sensores.
* **Base de Datos Time-Series:** Integración optimizada con **PostgreSQL + TimescaleDB** para almacenamiento masivo.
* **Detección en Tiempo Real:** Análisis automático de variables (Temperatura > 35°C, Humedad < 30%, Humo > 200ppm).
* **Arquitectura Distribuida:** Diseñado para conectarse a una capa de datos externa (Azure VM separada).

## Requisitos Previos

* Python 3.10+
* Base de Datos PostgreSQL 14+ con extensión TimescaleDB activa.
* Acceso de red (Puerto 5432) a la VM de Base de Datos.
