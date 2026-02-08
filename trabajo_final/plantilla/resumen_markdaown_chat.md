# Documento de Traspaso – Infraestructura Docker + Spark

## 1. Contexto y objetivo

El entorno implementa una infraestructura mínima de Big Data para el trabajo final del curso “Big Data con Python”, basada en Docker, Apache Spark y PostgreSQL.[file:1]  
El objetivo es disponer de un mini–clúster Spark distribuido (1 master, 1 worker) y una base de datos PostgreSQL trabajando sobre datos almacenados en un SSD externo en `F:\LABSTORAGE\`.[file:1]

---

## 2. Arquitectura general

- **Tecnologías principales**:
  - Docker Desktop sobre Windows con backend WSL2.[file:1]
  - Docker Compose para orquestación de servicios.[file:1]
  - Apache Spark 3.5.4 (`apache/spark:3.5.4-python3`).[file:1]
  - PostgreSQL 15 (`postgres:15-alpine`).[file:1]
- **Servicios desplegados**:
  - `postgres`: base de datos para resultados.
  - `spark-master`: coordinador del clúster.
  - `spark-worker_1`: nodo de cómputo (2 cores, 6 GiB RAM).
- **Red**:
  - Red bridge `spark-network`, que permite resolver servicios por nombre (`spark-master`, `postgres`, etc.).[file:1]

---

## 3. Estructura de almacenamiento en disco

Todo el almacenamiento persistente reside en el SSD externo `F:`:

```text
F:\LABSTORAGE\
├── data\             # Datos de entrada (qog_std_ts_jan24.csv)
├── postgres_data\    # Datos persistentes de PostgreSQL
├── spark_logs\       # Logs de Spark
└── spark_output\     # Resultados (Parquet, etc.)
data: contiene el dataset QoG usado en el proyecto.[file:1]

postgres_data: volumen mapeado a /var/lib/postgresql/data.[file:1]

spark_logs y spark_output: facilitan depuración y reutilización de resultados generados por Spark.[file:1]

4. docker-compose.yml
4.1 Servicio postgres
Rol: base de datos de resultados y tablas analíticas.[file:1]

text
postgres:
  image: postgres:15-alpine
  container_name: bigdata_postgres
  environment:
    POSTGRES_DB: bigdata
    POSTGRES_USER: spark_user
    POSTGRES_PASSWORD: spark_password
  ports:
    - "5432:5432"
  volumes:
    - F:/LABSTORAGE/postgres_data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U spark_user -d bigdata"]
    interval: 10s
    timeout: 5s
    retries: 5
  networks:
    - spark-network
  restart: unless-stopped
Healthcheck con pg_isready para evitar conexiones prematuras desde otros servicios.[file:6]

4.2 Servicio spark-master
Rol: coordinador del clúster y punto central de administración.[file:1]

text
spark-master:
  image: apache/spark:3.5.4-python3
  container_name: spark_master
  environment:
    - SPARK_MASTER_HOST=spark-master
    - SPARK_MASTER_PORT=7077
    - SPARK_MASTER_WEBUI_PORT=8080
  ports:
    - "8080:8080"      # Spark UI
    - "7077:7077"      # Puerto para workers y clientes
  volumes:
    - F:/LABSTORAGE/data:/opt/spark/work-dir/data
    - F:/LABSTORAGE/spark_output:/opt/spark/work-dir/output
    - F:/LABSTORAGE/spark_logs:/opt/spark/work-dir/logs
  command: >
    /opt/spark/bin/spark-class
    org.apache.spark.deploy.master.Master
  networks:
    - spark-network
  restart: unless-stopped
UI accesible en http://localhost:8080 para monitorizar jobs y workers.[file:1]

4.3 Servicio spark-worker_1
Rol: ejecutar tareas de cómputo distribuido.[file:1]

text
spark-worker:
  image: apache/spark:3.5.4-python3
  container_name: spark_worker_1
  environment:
    - SPARK_MODE=worker
    - SPARK_MASTER_URL=spark://spark-master:7077
  depends_on:
    - spark-master
  volumes:
    - F:/LABSTORAGE/data:/opt/spark/work-dir/data
    - F:/LABSTORAGE/spark_output:/opt/spark/work-dir/output
    - F:/LABSTORAGE/spark_logs:/opt/spark/work-dir/logs
  command: >
    /opt/spark/bin/spark-class
    org.apache.spark.deploy.worker.Worker
    spark://spark-master:7077
    --cores 2
    --memory 6g
  networks:
    - spark-network
  restart: unless-stopped
Recursos asignados: 2 cores, 6 GiB de RAM.[file:1]

Registro correcto con el master verificado en logs:
Successfully registered with master spark://spark-master:7077.[file:6]

4.4 Red
text
networks:
  spark-network:
    driver: bridge
Simplifica la comunicación interna mediante nombres de servicio en lugar de IPs.[file:1]

5. Ciclo de vida operativo
5.1 Arranque del clúster
Desde la carpeta donde está docker-compose.yml:

bash
docker compose up -d
Resultados esperados:[file:1]

Creación de la red spark-network.

Arranque de bigdata_postgres, spark_master, spark_worker_1.

Descarga de imágenes solo la primera vez.

Verificaciones:

bash
docker ps            # 3 contenedores en estado Up
docker logs spark_worker_1
# Debe incluir: "Successfully registered with master spark://spark-master:7077"
Spark UI:

Navegador → http://localhost:8080

Debe aparecer 1 worker “ALIVE”, 2 cores, 6 GiB de memoria.[file:6]

5.2 Parada y reinicio
Parar el clúster (sin borrar datos):

bash
docker compose down
Reanudar sesión conservando datos, logs y resultados:

bash
docker compose up -d
Los volúmenes mapeados a F:\LABSTORAGE\ garantizan persistencia entre sesiones.[file:1]

6. Integración con el pipeline ETL
Spark leerá el CSV QoG desde /opt/spark/work-dir/data/qog_std_ts_jan24.csv, mapeado desde F:\LABSTORAGE\data\qog_std_ts_jan24.csv.[file:1]

El script pipeline.py creará una SparkSession, filtrará países y años, generará variables derivadas y escribirá resultados en Parquet bajo /opt/spark/work-dir/output (F:\LABSTORAGE\spark_output).[file:1]

Los resultados agregados podrán persistirse en PostgreSQL vía JDBC usando las credenciales definidas en el servicio postgres.[file:1]

7. Decisiones de diseño y justificación
Imágenes oficiales (apache/spark:3.5.4-python3, postgres:15-alpine): alineadas con las recomendaciones del proyecto y fáciles de defender académicamente.[file:1]

Worker único con 2 cores y 6 GiB: equilibrio entre paralelismo y estabilidad en un host de 16 GiB.[file:1]

Healthcheck en PostgreSQL: evita condiciones de carrera si Spark intenta conectarse antes de que la base de datos esté lista.[file:6]

Separación de volúmenes: datos crudos, resultados, logs y base de datos aislados para facilitar mantenimiento.[file:1]

Red dedicada spark-network: facilita conexiones JDBC y registro de workers sin depender de IPs dinámicas.[file:1]

8. Recomendaciones para el nuevo responsable
Documentar cualquier cambio en docker-compose.yml dentro de 02_INFRAESTRUCTURA.md, explicando el motivo técnico.[file:6]

Antes de modificar memoria o cores del worker, revisar capacidad del host y tamaño de datasets previstos.[file:1]

Para depurar:

Revisar docker logs spark_master y docker logs spark_worker_1 ante ausencia de workers en la UI.[file:6]

Verificar permisos y existencia de rutas bajo F:\LABSTORAGE\ si hay errores de lectura/escritura.[file:1]

text
undefined