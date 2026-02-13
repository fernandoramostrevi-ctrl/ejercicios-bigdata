# Trabajo Final: "¿La dependencia de recursos petrolíferos está asociada con mayores niveles de corrupción y menor desarrollo humano en Asia Central? Análisis comparativo 2002-2021"

**Alumno:** Fernando Ramos
**Fecha:** 12/02/2026

---

## 🚀 Resultados Destacados (Executive Summary)
Para una revisión rápida del proyecto, accede directamente a los entregables finales:

| Entregable | Formato | Descripción |
|------------|---------|-------------|
| **[📄 Ver Informe Ejecutivo (PDF)](informes/Informe_Ejecutivo_Asia_Central.pdf)** | PDF | Informe gerencial completo con conclusiones y gráficas estáticas. |
| **[📈 Dashboard Interactivo (Live)](https://fernandoramostrevi-ctrl.github.io/ejercicios-bigdata/dashboard_asia_central.html)** | Web | *Click para ver online.* Visualización dinámica e interactiva de los datos. |

---

## Orden de trabajo

Completa los archivos en este orden. Cada numero indica la secuencia:

| Orden | Archivo | Que haces |
|-------|---------|-----------|
| **1** | `01_README.md` (este archivo) | Defines tu pregunta, paises y variables |
| **2** | `02_INFRAESTRUCTURA.md` | Construyes y explicas tu docker-compose.yml |
| **3** | `pipeline.py` | Escribes tu ETL + analisis con Spark |
| **4** | `03_RESULTADOS.md` | Presentas graficos e interpretas resultados |
| **5** | `04_REFLEXION_IA.md` | Documentas tu proceso y pegas tus prompts |
| **6** | `05_RESPUESTAS.md` | Respondes 4 preguntas de comprension |

Los archivos `docker-compose.yml`, `requirements.txt` y `.gitignore` los
completas conforme avanzas.

---

## Pregunta de investigacion

¿La dependencia de recursos petrolíferos está asociada con mayores niveles de corrupción y menor desarrollo humano en Asia Central? Análisis comparativo 2002-2021.

---

## Paises seleccionados (5)
| # | País         | Código ISO | Por qué lo elegiste                                                                                                                                                                                                                                                                                                                                                             |
| - | ------------ | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Kazajistán   | KAZ        | País más rico de Asia Central por recursos naturales (petróleo, gas, uranio). Alto PIB per cápita (~$12,500) pero alta corrupción. Ejemplo paradigmático de "maldición de recursos": crecimiento económico sin mejora institucional. Exportador clave hacia Rusia, China y Europa. Estrategia multivectorial más desarrollada.                                                  |
| 2 | Uzbekistán   | UZB        | Segundo país más poblado de la región. Economía basada en gas natural, algodón y oro. PIB medio (~$3,200). Transición política reciente (post-Karimov 2016) con reformas económicas parciales pero instituciones débiles. Pivote geográfico (fronterizo con todos los países centroasiáticos). Dependencia moderada de recursos permite comparación con extremos.               |
| 3 | Kirguistán   | KGZ        | País con menor dependencia de recursos naturales (principalmente oro e hidroeléctrica). PIB bajo (~$2,100) pero relativamente más democrático que vecinos. Permite contrastar hipótesis: ¿menos recursos = menos corrupción? Alta dependencia de remesas desde Rusia. Vulnerabilidad institucional a pesar de baja renta extractiva. Caso control para "maldición de recursos". |
| 4 | Tayikistán   | TJK        | País más pobre de Asia Central (PIB ~$1,800). Recursos limitados (aluminio, algodón, hidroeléctrica potencial). Altamente dependiente de remesas laborales. Permite analizar si pobreza extrema + pocos recursos = instituciones débiles por otros factores (guerra civil 1992-1997, geografía montañosa, aislamiento). Contraste con Kazajistán.                               |
| 5 | Turkmenistán | TKM        | Dependencia extrema de gas natural (~35-40% PIB de renta de recursos). Régimen autocrático hermético. Datos frecuentemente incompletos pero crítico para análisis de casos extremos. Si la maldición de recursos es real, Turkmenistán debe mostrar PIB moderado-alto con corrupción extrema. Representa el límite superior de "Estado rentista".                               |


---

## Variables seleccionadas (5 numericas)

| # | Variable              | Nombre en QoG     | Tipo       | Rol en el análisis                                          |
| - | --------------------- | ----------------- | ---------- | ----------------------------------------------------------- |
| 1 | País                  | cname             | Categórica | Identificador de cada país (5 valores)                      |
| 2 | Año                   | year              | Temporal   | Eje temporal del análisis (2000-2023)                       |
| 3 | Recursos Naturales    | wdi_totalresrent  | Numérica   | Variable independiente: Renta de recursos (% PIB)           |
| 4 | PIB per cápita        | wdi_gdpcapcon2017 | Numérica   | Variable dependiente 1: Desarrollo económico                |
| 5 | Control de Corrupción | wbgi_cce          | Numérica   | Variable dependiente 2: Calidad institucional               |
| 6 | Desarrollo Humano     | undp_hdi          | Numérica   | Variable dependiente 3: Bienestar ciudadano integral        |
| 7 | Esperanza de Vida     | wdi_lifexp        | Numérica   | Variable dependiente 4: Salud pública y condiciones de vida |
https://www.gu.se/en/quality-government/qog-data

---

## Variable derivada

| # | Variable Derivada                  | Fórmula                          | Motivo de Creación                                                                                                                                    |
| - | ---------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Brecha Corrupción-Riqueza          | PIB / (Corrupción + 3)           | Medir si la riqueza económica se traduce en buena gobernanza. Valores altos = país rico pero corrupto (riqueza no redistribuida institucionalmente).  |
| 2 | Eficiencia de Recursos             | PIB / Recursos Naturales         | Evaluar cuánto PIB genera cada país por unidad de recursos extractivos. Baja eficiencia = economía no diversificada y vulnerable a shocks de precios. |
| 3 | Índice de Bienestar Redistributivo | (PIB_norm + Corrupción_norm) / 2 | Crear métrica compuesta que combine desarrollo económico y calidad institucional. Captura si el crecimiento se traduce en bienestar ciudadano real.   |

---

## Tipo de analisis elegido

- [ ] Clustering (K-Means)
- [X] Serie temporal (evolucion por pais)
- [ ] Comparacion (antes/despues de un evento)

---

## Como ejecutar mi pipeline

El proyecto consta de una fase de procesamiento con Spark (ETL) y una fase de visualización con Dash/Plotly. Sigue estos pasos para reproducirlo tal exactitud:

### 0. Requisitos previos
- Tener Docker y Docker Compose instalados
- Tener Python 3.9+ instalado
- (Opcional) Crear un entorno virtual:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
```

### 1. Instalar dependencias
Instala las librerías necesarias para los scripts locales de visualización:
```bash
pip install -r trabajo_final/requirements.txt
```

### 2. Levantar infraestructura Spark
Arranca el clúster (Master + Workers) y la base de datos PostgreSQL:
```bash
cd trabajo_final/plantilla
docker compose up -d
```
> *Verifica que todo funciona con `docker ps` y accediendo a http://localhost:8080*

### 3. Ejecutar Pipeline ETL (Spark)
Este script procesa los datos crudos, los limpia y genera los archivos parquet/csv en `trabajo_final/output`.
```bash
python trabajo_final/plantilla/scripts/pipeline.py
```

### 4. Generar Dashboard y Reportes
Tienes dos opciones para visualizar los resultados:

**Opción A: Generar reportes estáticos (HTML)**
Genera gráficos individuales y un dashboard HTML completo en la carpeta `output`.
```bash
python trabajo_final/plantilla/scripts/dashboard.py
```
> *El archivo principal generado será `trabajo_final/output/dashboard_asia_central.html`*

**Opción B: Lanza el Dashboard Interactivo**
Levanta una aplicación web local con Dash donde puedes explorar los datos dinámicamente.
```bash
python trabajo_final/plantilla/scripts/dashboard_interactivo.py
```
> *Abre tu navegador en http://127.0.0.1:8050 para ver el dashboard interactivo.*

### 5. Limpieza (Opcional)
Para detener y eliminar los contenedores al finalizar:
```bash
docker compose down
```
