# Resumen Ejecutivo: Proyecto Big Data Asia Central (2000-2023)

**Fecha de inicio:** 06/02/2026  
**Última actualización:** 08/02/2026  
**Estudiante:** Fernando Ramos  
**Curso:** Especialista Big Data con Python

---

## 1. Contexto del Proyecto

### Pregunta de Investigación
¿La exportación de recursos naturales hacia Rusia, China y Europa determina el crecimiento económico y los niveles de corrupción en Asia Central? Análisis longitudinal (2000-2023)

### Objetivos del Proyecto
- Implementar infraestructura Big Data con Docker + Spark + PostgreSQL
- Desarrollar pipeline ETL con PySpark para análisis de 5 países de Asia Central
- Crear visualizaciones interactivas con Plotly
- Documentar proceso analítico siguiendo metodología de analista profesional

---

## 2. Infraestructura Implementada

### Stack Tecnológico
| Componente | Versión/Detalle |
|------------|-----------------|
| Docker Desktop | Backend WSL2 (Windows) |
| Apache Spark | 3.5.4 (imagen oficial `apache/spark:3.5.4-python3`) |
| PostgreSQL | 15-alpine |
| Python | 3.11 (downgrade desde 3.13 por incompatibilidad con PySpark) |
| PySpark | 3.5.4 |
| Pandas | Latest |
| Plotly | Para visualizaciones interactivas |

### Arquitectura Docker (`docker-compose.yml`)

**Servicios desplegados:**

1. **`postgres`** (bigdata_postgres)
   - Base de datos para resultados analíticos
   - Puerto: 5432
   - Credenciales: `spark_user` / `spark_password` / DB: `bigdata`
   - Volumen persistente: `F:\LABSTORAGE\postgres_data`
   - Healthcheck con `pg_isready`

2. **`spark-master`**
   - Coordinador del clúster Spark
   - Puerto UI: 8080 (http://localhost:8080)
   - Puerto interno: 7077
   - Volúmenes mapeados:
     - Datos: `F:\LABSTORAGE\data` → `/opt/spark/work-dir/data`
     - Salida: `F:\LABSTORAGE\spark_output` → `/opt/spark/work-dir/output`
     - Logs: `F:\LABSTORAGE\spark_logs` → `/opt/spark/work-dir/logs`

3. **`spark-worker_1`**
   - Nodo de cómputo
   - Recursos asignados: 2 cores, 6 GiB RAM
   - Registrado exitosamente con el master

**Red:** `spark-network` (driver bridge)

### Almacenamiento en Disco Externo (SSD F:\)
F:\LABSTORAGE
├── data\ # Dataset QoG (qog_std_ts_jan24.csv, 120 MB)
├── postgres_data\ # Datos persistentes PostgreSQL
├── spark_logs\ # Logs de Spark
└── spark_output\ # Resultados en Parquet

text

**Decisión de diseño:** Todo el almacenamiento persistente en SSD externo F:\ para:
- Separar datos de sistema operativo
- Facilitar backup
- Mantener datos entre sesiones Docker

---

## 3. Dataset y Variables

### Fuente de Datos
- **Dataset:** Quality of Government (QoG) Standard Time-Series (Enero 2024)
- **Archivo:** `qog_std_ts_jan24.csv`
- **Tamaño:** 120 MB, 15,564 filas totales
- **URL:** https://www.gu.se/en/quality-government/qog-data

### Países Seleccionados (5)
| País | Código ISO | Registros 2000-2023 | Justificación |
|------|------------|---------------------|---------------|
| Kazakhstan | KAZ | 24 | País más rico por recursos (petróleo, gas, uranio). Alto PIB (~$12,500) pero alta corrupción. Ejemplo de "maldición de recursos" |
| Kyrgyzstan | KGZ | 24 | Menor dependencia de recursos naturales (oro, hidroeléctrica). PIB bajo (~$2,100) pero más democrático. Caso control |
| Tajikistan | TJK | 24 | País más pobre (PIB ~$1,800). Recursos limitados. Alta dependencia de remesas. Contraste con Kazakhstan |
| Turkmenistan | TKM | 24 | Dependencia extrema de gas natural (35-40% PIB). Régimen autocrático. Caso extremo de Estado rentista |
| Uzbekistan | UZB | 24 | Economía basada en gas, algodón, oro. PIB medio (~$3,200). Transición política post-Karimov (2016) |

**Total registros filtrados:** 120 (5 países × 24 años) ✅

### Variables del QoG Utilizadas

**Variables Base (7):**
| # | Variable | Nombre en QoG | Tipo | Descripción |
|---|----------|---------------|------|-------------|
| 1 | País | `cname` | Categórica | Identificador (valores confirmados: Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan) |
| 2 | Año | `year` | Temporal | 2000-2023 |
| 3 | Recursos Naturales | `wdi_totalresrent` | Numérica | Renta de recursos naturales (% PIB) - Variable independiente |
| 4 | PIB per cápita | `wdi_gdpcapcon2017` | Numérica | USD constantes 2017 - Variable dependiente 1 |
| 5 | Control de Corrupción | `wbgi_cce` | Numérica | Índice Banco Mundial (escala -2.5 a +2.5, valores altos = MENOS corrupción) - Variable dependiente 2 |
| 6 | Desarrollo Humano | `undp_hdi` | Numérica | Índice PNUD (0-1) - Variable dependiente 3 |
| 7 | Esperanza de Vida | `wdi_lifexp` | Numérica | Años al nacer - Variable dependiente 4 |

**Variables Derivadas (4):**
| # | Variable | Fórmula | Propósito |
|---|----------|---------|-----------|
| 1 | Corrupción Invertida | `-wbgi_cce` | Invertir escala para que valores altos = más corrupción (más intuitivo para visualización) |
| 2 | Brecha Corrupción-Riqueza | `PIB / (Corrupción_invertida + 3)` | Medir si riqueza económica se traduce en buena gobernanza |
| 3 | Eficiencia de Recursos | `PIB / Recursos_Naturales` | Cuánto PIB genera cada país por unidad de recursos. Baja eficiencia = economía no diversificada |
| 4 | Índice de Bienestar Redistributivo (2 versiones) | `(PIB_norm + Corrupción_norm) / 2` | - **Global:** Normalización min/max de los 5 países (comparar niveles absolutos)<br>- **Por país:** Normalización por país (ver evolución relativa interna) |

---

## 4. Pipeline ETL (pipeline.py)

### Diseño del Pipeline (10 pasos)

**BLOQUE 1: Extracción y Filtrado**
1. Inicializar SparkSession (local[*], 4GB driver memory, 8 shuffle partitions)
2. Leer CSV completo (15,564 filas, inferSchema=True, encoding=utf-8)
3. Filtrar países de Asia Central y período 2000-2023 → 120 registros
4. Seleccionar 7 columnas relevantes

**BLOQUE 2: Limpieza y Transformación**
5. Renombrar columnas a nombres legibles (español)
6. Análisis de nulos:
   - Estrategia: Imputar por media del país si <20% nulos
   - Si >20% nulos: mantener NaN visible (importante para Turkmenistán con datos fragmentados)
7. Crear variable `corrupcion_invertida = -wbgi_cce`
8. Crear 3 variables derivadas (Brecha, Eficiencia, Bienestar Global y Por País)

**BLOQUE 3: Persistencia**
9. Guardar en Parquet:
   - `datos_limpios.parquet` (tabla fact con todas las variables)
   - `agregados_por_pais.parquet` (medias 2000-2023 por país)
   - `series_temporales.parquet` (formato largo para Plotly: país, año, variable, valor)
10. Generar estadísticas descriptivas:
    - Matriz de correlación (para heatmap)
    - Estadísticas por país (min, max, media, std)
    - Exportar CSV para inspección manual

### Configuración Especial para Windows
```python
import os
import sys

# Solución problema HADOOP_HOME en Windows
os.environ['HADOOP_HOME'] = r'C:\hadoop'
sys.path.append(r'C:\hadoop\bin')
Requisito: Descargar winutils.exe de https://github.com/cdarlint/winutils y colocar en C:\hadoop\bin\

5. Problemas Resueltos y Decisiones Técnicas
Problema 1: Python 3.13 incompatible con PySpark 3.5.4
Error inicial:

text
TypeError: code() argument 13 must be str, not int
Causa: PySpark 3.5.4 no soporta oficialmente Python 3.13.

Solución aplicada:

Downgrade a Python 3.11 (descargado desde python.org, NO Microsoft Store)

Crear nuevo entorno virtual: .venv_311

Reinstalar todas las dependencias con pip install -r requirements.txt

Lección: Para proyectos académicos con entregas, usar versiones estables y verificadas del stack.

Problema 2: Python de Microsoft Store con limitaciones
Error:

text
ModuleNotFoundError: No module named 'jaraco'
setuptools failed to import in the build environment
Causa: Python instalado desde Microsoft Store (WindowsApps) tiene restricciones de permisos y problemas con pip.

Solución:

Instalar Python 3.11 desde python.org

Instalación: "Add to PATH" + "Install for all users" en C:\Python311

Evitar usar Python de WindowsApps para desarrollo

Problema 3: JUNCTION no accesible desde entorno remoto
Situación: El JUNCTION entre C:\Users\...\PycharmProjects\ejercicios-bigdata\ y F:\LABSTORAGE\ funciona localmente pero no desde entornos remotos (ej. servidor de Perplexity).

Solución:

Scripts de exploración ejecutados localmente en PyCharm

Pipeline usa rutas absolutas directas: F:/LABSTORAGE/data/qog_std_ts_jan24.csv

Confirmación manual de nombres de países en el CSV antes de codificar filtros

Script de exploración utilizado:

python
import pandas as pd
csv_path = "F:/LABSTORAGE/data/qog_std_ts_jan24.csv"
df_explore = pd.read_csv(csv_path, usecols=['cname', 'year'])
# Filtrar y verificar países de Asia Central
Resultado: Confirmados 5 países con 24 registros cada uno (2000-2023) ✅

Problema 4: Error HADOOP_HOME en Windows al escribir Parquet
Error:

text
java.io.FileNotFoundException: HADOOP_HOME and hadoop.home.dir are unset
Causa: Spark requiere binarios de Hadoop (winutils.exe) para operaciones de archivo en Windows.

Solución:

Descargar winutils.exe de https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.5/bin/winutils.exe

Crear carpeta C:\hadoop\bin\ y colocar winutils.exe

Configurar variables de entorno en pipeline.py:

python
os.environ['HADOOP_HOME'] = r'C:\hadoop'
sys.path.append(r'C:\hadoop\bin')
6. Visualizaciones Planificadas (Plotly)
Tipos de Gráficos Definidos
Series temporales (líneas): Evolución de PIB, corrupción, recursos naturales por país (2000-2023)

Histogramas: Distribución de variables derivadas (Brecha Corrupción-Riqueza, Eficiencia de Recursos)

Mapa de calor (heatmap): Correlación entre variables numéricas

Gráficos de dispersión (scatter): Recursos Naturales (X) vs. Control de Corrupción (Y), coloreado por país

Boxplots: Comparar distribuciones de variables entre los 5 países

Requisitos de visualización:

Títulos descriptivos

Ejes etiquetados (español)

Leyendas claras

Interactividad Plotly (filtros por país, variable, año)

7. Estado Actual del Proyecto
✅ Completado
 Infraestructura Docker (Spark + PostgreSQL) funcional

 Dataset QoG descargado y verificado (120 registros confirmados)

 Nombres exactos de países confirmados en CSV

 Entorno Python 3.11 configurado con dependencias instaladas

 Pipeline ETL completo desarrollado (pipeline.py)

 Problema HADOOP_HOME resuelto (winutils.exe configurado)

 Variables derivadas definidas con justificación analítica

🚧 Pendiente
 Ejecutar pipeline completo y validar salida Parquet

 Crear scripts de visualización con Plotly

 Análisis estadístico (correlaciones, tendencias)

 Documentación académica:

 02_INFRAESTRUCTURA.md (explicar docker-compose.yml)

 03_RESULTADOS.md (interpretar gráficos)

 04_REFLEXION_IA.md (documentar prompts y aprendizajes)

 05_RESPUESTAS.md (preguntas de comprensión)

 Carga de resultados a PostgreSQL vía JDBC (opcional)

8. Metodología de Trabajo Aplicada
Principios Seguidos
Verificación antes de codificación: Confirmar nombres de países, estructura de datos, tipos de columnas antes de escribir pipeline

Validación por bloques: No avanzar al siguiente paso hasta confirmar que el anterior funciona

Pensamiento analítico: Definir fórmulas de variables derivadas con justificación de negocio, no solo técnica

Documentación continua: Explicar decisiones (ej. por qué invertir escala de corrupción, por qué 2 versiones del índice de bienestar)

Gestión de errores proactiva: Detectar incompatibilidades de versiones antes de invertir tiempo en código complejo

Buenas Prácticas Implementadas
Nombres de variables descriptivos en español (legibilidad para análisis)

Separación de datos crudos, procesados y logs en volúmenes Docker

Uso de Parquet para eficiencia en análisis posteriores

Healthchecks en PostgreSQL para evitar condiciones de carrera

Configuración explícita de recursos Spark (memoria, cores, partitions)

9. Comandos de Ejecución
Iniciar Infraestructura
bash
# Levantar contenedores Docker
cd [carpeta con docker-compose.yml]
docker compose up -d

# Verificar estado
docker ps

# Ver logs
docker logs spark_master
docker logs spark_worker_1
docker logs bigdata_postgres

# Acceder a Spark UI
# Navegador: http://localhost:8080
Ejecutar Pipeline ETL
bash
cd C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\trabajo_final
.venv_311\Scripts\activate
python pipeline.py
Detener Infraestructura (sin perder datos)
bash
docker compose down
10. Archivos del Proyecto
text
C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\trabajo_final\
│
├── .venv_311\                    # Entorno virtual Python 3.11
├── plantilla\
│   └── scripts\
│       ├── pipeline.py           # Pipeline ETL principal ✅
│       └── explorar_paises.py    # Script de verificación ✅
│
├── docker-compose.yml            # Orquestación Spark + PostgreSQL ✅
├── requirements.txt              # Dependencias Python ✅
├── 01_README.md                  # Definición del proyecto ✅
├── 02_INFRAESTRUCTURA.md         # 🚧 Pendiente
├── 03_RESULTADOS.md              # 🚧 Pendiente
├── 04_REFLEXION_IA.md            # 🚧 Pendiente
└── 05_RESPUESTAS.md              # 🚧 Pendiente

F:\LABSTORAGE\
├── data\
│   └── qog_std_ts_jan24.csv      # Dataset original ✅
├── spark_output\                 # 🚧 Parquets generados por pipeline
├── spark_logs\                   # Logs de ejecución
└── postgres_data\                # Datos persistentes PostgreSQL

C:\hadoop\bin\
└── winutils.exe                  # Binario Hadoop para Windows ✅
11. Decisiones de Diseño Justificadas
Normalización del Índice de Bienestar: Global vs. Por País
Decisión: Crear DOS versiones de la variable derivada.

Justificación:

Global: Permite comparar niveles absolutos entre países (¿quién está mejor/peor en la región?)

Por país: Permite ver evolución relativa dentro de cada país (¿ha mejorado Turkmenistán respecto a sí mismo en 2000?)

Ambas perspectivas son relevantes para la pregunta de investigación

Inversión de la escala de corrupción (wbgi_cce)
Decisión: Crear corrupcion_invertida = -wbgi_cce

Justificación:

Escala original del Banco Mundial: valores altos = MENOS corrupción (contraintuitivo)

Para gráficos y análisis: mejor que valores altos = MÁS corrupción

Facilita interpretación visual (líneas ascendentes = empeoramiento institucional)

Se documenta claramente en leyendas de gráficos para transparencia

Estrategia de nulos: 20% como umbral
Decisión: Imputar por media del país si <20% nulos; mantener NaN si >20%

Justificación:

Turkmenistán tiene datos frecuentemente incompletos (régimen hermético)

Imputar masivamente falsearía la realidad institucional del país

Mantener NaN visible en gráficos refleja la opacidad del régimen (dato en sí mismo)

Umbral 20% basado en recomendaciones académicas estándar

Almacenamiento en SSD externo (F:)
Decisión: Todo el almacenamiento persistente en F:\LABSTORAGE\ en lugar de disco sistema

Justificación:

Separar datos de proyecto de sistema operativo (seguridad)

Facilitar backups (copiar carpeta completa)

Evitar pérdida de datos si se reinstala SO

Mejora rendimiento I/O (SSD dedicado)

Mantiene datos entre sesiones Docker sin ocupar espacio en C:\

12. Próximos Pasos Recomendados
Inmediato (próxima sesión)
Ejecutar pipeline.py completo y verificar generación de Parquets en F:\LABSTORAGE\spark_output\

Inspeccionar salida: Abrir Parquets con Pandas y validar:

120 registros en datos_limpios.parquet

Valores correctos de variables derivadas (sin NaN inesperados, sin divisiones por cero)

Rangos de valores lógicos (ej. PIB > 0, Corrupción Invertida en rango esperado)

Corto plazo (1-2 días)
Crear script de visualización (visualizaciones.py):

Leer Parquets generados

Generar 5 tipos de gráficos Plotly definidos

Exportar como HTML interactivos o PNG estáticos

Análisis estadístico básico:

Matriz de correlación entre variables

Pruebas de tendencias temporales (ej. regresión lineal simple por país)

Identificar outliers y valores atípicos

Medio plazo (3-5 días)
Documentación académica:

Completar 02_INFRAESTRUCTURA.md (explicar docker-compose.yml con capturas de Spark UI)

Completar 03_RESULTADOS.md (pegar gráficos, interpretar hallazgos, responder pregunta de investigación)

Completar 04_REFLEXION_IA.md (pegar prompts clave usados, errores resueltos, aprendizajes)

Completar 05_RESPUESTAS.md (preguntas de comprensión del profesor)

Opcional: Implementar carga a PostgreSQL vía JDBC (crear tablas agregadas SQL para consultas ad-hoc)

13. Contactos y Recursos Clave
Documentación Utilizada
Quality of Government Dataset: https://www.gu.se/en/quality-government/qog-data

PySpark 3.5.4 Docs: https://spark.apache.org/docs/3.5.4/

Hadoop Windows Problems: https://cwiki.apache.org/confluence/display/HADOOP2/WindowsProblems

Winutils GitHub: https://github.com/cdarlint/winutils

Archivos de Configuración Clave
requirements.txt: PySpark==3.5.4, pandas, plotly, matplotlib, seaborn, psycopg2, pyarrow, scikit-learn

docker-compose.yml: 3 servicios (postgres, spark-master, spark-worker), red spark-network

Fin del Resumen Ejecutivo

Última actualización: 08/02/2026, 17:55 CET
Versión: 1.0
Estado del proyecto: Pipeline ETL completado ✅ | Visualizaciones y documentación pendientes 🚧

text

***

**Este documento contiene todo el contexto necesario para continuar el proyecto en un nuevo chat.** Incluye:
- Decisiones técnicas justificadas
- Problemas resueltos con soluciones documentadas
- Estructura completa del proyecto
- Estado actual y próximos pasos
- Comandos de ejecución