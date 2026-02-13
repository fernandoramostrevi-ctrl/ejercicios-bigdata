# Registro de Prompts - Trabajo Final

**Alumno:** Fernando Ramos
**Fecha:** 13/02/2026
**IA utilizada:** Gemini / ChatGPT / Perplexity

---

## COMO USAR ESTE ARCHIVO

Este archivo tiene **DOS PARTES** muy diferentes:

| Parte | Que es | Como debe verse |
|-------|--------|-----------------|
| **PARTE 1** | Mis 3 prompts reales | Lenguaje NATURAL, con errores, informal |
| **PARTE 2** | Blueprint generado por IA | Perfecto, profesional, estructurado |

---

# PARTE 1: Mis Prompts Reales (3 minimo)

## Prompt A: Infraestructura Docker

**Contexto:** Necesitaba configurar el entorno de trabajo distribuido en un disco duro externo.

**Mi prompt exacto (copiado tal cual):**
```
necesito crear un cluster distribuido con Spark y docker. genera un archivo .yml para Tengo un disco SSD externo de 250 GB en el puerto F: de mi ordenador. Mi equipo tiene 16 gb de ram y dos nucleos, quiero crear un maestro y dos trabajadores y mi base de datos esta en esta ruta F:\LABSTORAGE\data
```

**Que paso:** [x] Funciono  [ ] Funciono parcial  [ ] No funciono

**Que aprendi:** Aprendí cómo mapear volúmenes locales a rutas específicas dentro de contenedores y la importancia de la coordinación entre el nodo Master y los Workers.

---

## Prompt B: Pipeline ETL / Spark

**Contexto:** Solución de errores en el entorno de Windows para ejecutar PySpark.

**Mi prompt exacto (copiado tal cual):**
```
revisa por favor los .md que estan la arpeta C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\trabajo_final se que en algunoindica que como se han de tratar los vlores nulos
```

**Que paso:** [ ] Funciono  [x] Funciono parcial  [ ] No funciono

**Que aprendi:** Aunque el prompt no resolvió directamente el error técnico, me llevó a descubrir que las columnas del dataset oficial tenían nombres distintos a los que yo pensaba, lo cual desbloqueó el pipeline.

---

## Prompt C: Analisis / Graficos

**Contexto:** Definición de requisitos estéticos y funcionales para los gráficos interactivos.

**Mi prompt exacto (copiado tal cual):**
```
antes de generar el archivo.py tenemos que asegurarnos de que los graficos cumplen con los requisitos adecuados. Los graficos tienen que ser profesionales. Visualmente atractivos, letras de los indices y titulos legibles y sin superponerse. Graficos dinamicos es un punto fuerte, permitir al usuario cambiar entre paises o rangos de tiempo. Para cada grafico propuesto te voy a pasar consejos y ejemplos que he encontrado. Empezamos por los Grafico de regresion...
```

**Que paso:** [x] Funciono  [ ] Funciono parcial  [ ] No funciono

**Que aprendi:** Aprendí que dar instrucciones detalladas como si fuera un diseñador mejora drásticamente la calidad visual de Plotly y la utilidad de los tooltips interactivos.

---

# PARTE 2: Blueprint Replicable (generado por IA)

## Mi Blueprint

**Prompt que use para generar esto:**
```
Genera un prompt profesional tipo blueprint que describa exactamente lo que logramos: stack, tecnologias, arquitectura, datos y pasos. Debe ser tan detallado que si se lo paso a otra IA o a un desarrollador senior, pueda replicar el proyecto completo sin ver mi codigo.
```

**Blueprint generado por la IA:**

```
PROYECTO: Impacto de los Recursos Naturales en la Economía y Corrupción de Asia Central (2000-2023)

INFRAESTRUCTURA (Docker Compose):
- Sistema basado en Spark 3.5.0.
- Master Node: bitnami/spark:3.5.0 (puertos 8080 UI, 7077 Master).
- Worker Nodes: 2 réplicas (1GB RAM, 1 Core cada uno).
- PostgreSQL 15: Almacenamiento persistente.
- Volúmenes: Persistencia externa para portabilidad de datos.

DATOS:
- Dataset: Quality of Government (QoG) Standard Time-Series Dataset (Enero 2024).
- Paises: KAZ, KGZ, TJK, TKM, UZB.
- Variables: wdi_oilrent, wdi_gdpcapcon2017, wbgi_cce, undp_hdi.

PIPELINE ETL (PySpark):
1. Extracción: Carga de CSV masivo en Spark DataFrame.
2. Limpieza: Manejo de nulos ("NA", "..") y filtrado regional.
3. Transformación: 
   - Cálculo de Eficiencia de Recursos (PIB/Renta).
   - Generación de Índice de Bienestar Redistributivo (Normalización).
4. Carga: Exportación a Parquet (rendimiento) y CSV (visualización).

ANÁLISIS Y VISUALIZACIÓN:
- Dashboard interactivo (Pandas + Plotly).
- Gráficos: Evolución PIB (Log), Scatters de Correlación con línea de regresión, Heatmap de variables.

TECNOLOGÍAS:
- Python 3.11, PySpark 3.5.0, Pandas, Plotly, Docker Compose.

COMANDO PARA EJECUTAR:
docker compose up -d && python scripts/pipeline.py && python scripts/dashboard_profesional.py
```

---

## Verificacion de Coherencia

| Pregunta | Tu respuesta |
|----------|--------------|
| La version de Spark en el blueprint coincide con tu docker-compose.yml? | Si |
| Los paises del blueprint son los mismos que filtra tu pipeline.py? | Si |
| Las variables del blueprint estan en tu codigo? | Si |
| El tipo de analisis del blueprint coincide con tus graficos? | Si |

---

## Estadisticas Finales

| Metrica | Valor |
|---------|-------|
| Total de interacciones con IA (aprox) | 45 |
| Prompts que funcionaron a la primera | 30 |
| Errores que tuve que resolver | 12 |
| Horas totales de trabajo | 25 |

---

## Declaracion

[x] Confirmo que los prompts de la PARTE 1 son reales y no fueron modificados ni pasados por IA para corregirlos.

[x] Confirmo que el blueprint de la PARTE 2 fue generado por IA basandose en mi proyecto real.

[x] Entiendo que inconsistencias entre el blueprint y mi codigo seran investigadas.

---

## Capturas de Pantalla (Evidencias)

Las capturas de los prompts y del entorno se encuentran en la carpeta `capturas/`:

1. **Prompt de Infraestructura:** `capturas/spark_master.png`
2. **Contexto Principal:** `capturas/Instrucciones_principales.png`

---

**Nombre:** Fernando Ramos
**Fecha:** 13/02/2026
