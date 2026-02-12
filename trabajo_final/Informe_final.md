Informe Ejecutivo: Recursos Naturales, Crecimiento Económico y Corrupción en Asia Central (2000-2021)
Autor: Fernando Ramos Fecha: 09/02/2026
1. Introducción y Pregunta de Investigación
Este informe presenta los hallazgos de un análisis longitudinal sobre la relación entre la dotación de recursos naturales, el crecimiento económico y los niveles de corrupción en los cinco países de Asia Central: Kazajistán, Kirguistán, Tayikistán, Turkmenistán y Uzbekistán. El período de estudio abarca desde el año 2000 hasta el 2021.
La pregunta de investigación central que guía este estudio es: "¿La exportación de recursos naturales hacia Rusia, China y Europa determina el crecimiento económico y los niveles de corrupción en Asia Central?"
Para abordar esta cuestión, se ha desarrollado un pipeline ETL robusto y un dashboard interactivo que visualiza las tendencias y correlaciones clave.
2. Metodología: Pipeline ETL con Apache Spark
El procesamiento de los datos se realizó mediante un pipeline ETL (Extracción, Transformación, Carga) implementado en Python utilizando la librería Apache Spark. Este enfoque garantiza la escalabilidad y eficiencia en el manejo de grandes volúmenes de datos.
2.1. Extracción de Datos:
•
Fuente: El dataset principal es el "Quality of Government Standard Dataset (QoG)" de enero de 2024, almacenado en qog_std_ts_jan24.csv.
•
Filtrado: Se seleccionaron únicamente los registros correspondientes a los cinco países de Asia Central y al período 2000-2021.
2.2. Transformación de Datos:
•
Selección de Variables Clave: Se identificaron y seleccionaron las siguientes variables del dataset QoG, renombrándolas para mayor claridad:
◦
cname (País)
◦
year (Año)
◦
wdi_oilrent (Renta de recursos naturales como proxy de wdi_totalresrent)
◦
wdi_gdpcappppcon2017 (PIB per cápita PPA, proxy de wdi_gdpcapcon2017)
◦
wbgi_cce (Control de Corrupción)
◦
undp_hdi (Índice de Desarrollo Humano)
◦
wdi_lifexp (Esperanza de Vida)
•
Limpieza de Datos:
◦
Se implementó un proceso de limpieza para manejar valores faltantes ("NA", "..", "") en las columnas numéricas, convirtiéndolos a NULL.
◦
Las filas con NULL en variables críticas (wdi_gdpcapcon2017, wbgi_cce, wdi_totalresrent) fueron eliminadas para asegurar la integridad de los cálculos.
•
Creación de Variables Derivadas: Se calcularon tres nuevas métricas para un análisis más profundo:
◦
Brecha Corrupción-Riqueza: PIB / (Corrupción + 3). Esta métrica busca identificar si la riqueza económica se traduce en una mejor gobernanza.
◦
Eficiencia de Recursos: PIB / Recursos Naturales. Mide cuánto PIB genera un país por unidad de recurso natural.
◦
Índice de Bienestar Redistributivo: (PIB_norm + Corrupción_norm) / 2. Una métrica compuesta que combina desarrollo económico y calidad institucional, normalizando ambas variables entre 0 y 1.
2.3. Carga de Datos:
•
Los datos procesados y transformados se cargaron en formato Parquet (asia_central_processed) y CSV (asia_central_processed_csv) para facilitar su posterior análisis y visualización.
3. Análisis y Visualización
El análisis de los resultados se presenta a través de una serie de visualizaciones generadas con Plotly.
3.1. Pestaña 1: "Recursos y Economía"
•
Gráfico 1: Scatter Plot "Recursos Naturales vs PIB per cápita"
◦
Descripción: Este gráfico de dispersión muestra la relación entre el porcentaje del PIB proveniente de recursos naturales y el PIB per cápita de cada país a lo largo del tiempo. El eje Y utiliza una escala logarítmica para visualizar mejor las grandes diferencias en el PIB.
◦
Hallazgo: Se observa una correlación positiva fuerte (r ≈ 0.551). Esto sugiere que, en la región de Asia Central, una mayor dependencia de los recursos naturales se asocia con un PIB per cápita más elevado. Los países con mayores rentas de recursos (como Kazajistán y Turkmenistán) tienden a tener un PIB per cápita superior.
◦
Interpretación: Los recursos naturales son un motor significativo del crecimiento económico en estos países.
!Recursos vs PIB
•
Gráfico 2: Serie Temporal "Evolución PIB per cápita 2000-2021"
◦
Descripción: Un gráfico de líneas que traza la evolución del PIB per cápita para cada país a lo largo del período de estudio, también con escala logarítmica en el eje Y. Incluye una línea vertical para señalar la crisis financiera de 2008.
◦
Hallazgo: Se evidencia una creciente divergencia económica entre los países. Mientras que Kazajistán muestra un crecimiento sostenido, otros países como Tayikistán y Kirguistán se mantienen en niveles de PIB per cápita significativamente más bajos. La crisis de 2008 tuvo un impacto visible, pero la recuperación y el patrón de divergencia persistieron.
◦
Interpretación: A pesar de la dependencia de recursos, la trayectoria económica no es uniforme, y factores internos o externos han acentuado las diferencias.
!Evolución PIB
3.2. Pestaña 2: "Gobernanza y Eficiencia"
•
Gráfico 3: Scatter Plot "Recursos Naturales vs Control de Corrupción"
◦
Descripción: Este gráfico de dispersión explora la relación entre la renta de recursos naturales y el índice de Control de Corrupción del Banco Mundial (donde valores más altos indican menos corrupción).
◦
Hallazgo: La correlación observada es débil (r ≈ 0.208). No se encuentra una relación lineal fuerte que sugiera que una mayor dotación de recursos naturales esté directamente asociada con mayores niveles de corrupción (la "maldición de recursos" en su forma más simple).
◦
Interpretación: La "maldición de recursos" no se manifiesta de forma directa y lineal en la correlación simple. Otros factores institucionales y políticos podrían estar influyendo en los niveles de corrupción, más allá de la mera presencia de recursos.
!Recursos vs Corrupción
•
Gráfico 4: Barras "Eficiencia de Recursos por País (promedio 2000-2021)"
◦
Descripción: Un gráfico de barras horizontales que muestra la eficiencia promedio de cada país en generar PIB por unidad de recurso natural, utilizando una escala logarítmica para el eje de eficiencia.
◦
Hallazgo: Los países con menor dependencia de recursos naturales (como Kirguistán y Tayikistán) tienden a mostrar una mayor eficiencia de recursos. Por el contrario, países con alta dotación de recursos (como Turkmenistán y Kazajistán) pueden ser menos eficientes, lo que sugiere una menor diversificación económica.
◦
Interpretación: Una alta dependencia de recursos puede llevar a una menor presión para diversificar la economía y mejorar la eficiencia en otros sectores, lo que podría ser una manifestación más sutil de la "maldición de recursos".
!Eficiencia de Recursos
3.3. Pestaña 3: "Correlaciones"
•
Gráfico 5: Heatmap "Matriz de Correlación - Variables Clave"
◦
Descripción: Un mapa de calor que visualiza la matriz de correlación de todas las variables clave del estudio, incluyendo las derivadas. Los colores indican la fuerza y dirección de la correlación.
◦
Hallazgo: Este gráfico ofrece una visión holística de las interrelaciones. Se confirman las correlaciones fuertes ya observadas (ej., Recursos-PIB) y se revelan otras relaciones, como la correlación positiva entre PIB per cápita y Desarrollo Humano, o la relación entre Control de Corrupción y el Índice de Bienestar Redistributivo.
◦
Interpretación: Permite identificar patrones complejos y variables que se mueven conjuntamente, sirviendo como base para futuras investigaciones sobre causalidad.
!Matriz de Correlación
4. Conclusión Final
El análisis de los países de Asia Central entre 2000 y 2021 revela una relación compleja con sus recursos naturales:
•
Impacto Económico Directo: Los recursos naturales son un motor innegable del crecimiento económico, con una correlación positiva fuerte con el PIB per cápita.
•
Ausencia de "Maldición de Recursos" Simple: La hipótesis de la "maldición de recursos" no se confirma de manera directa a través de una correlación fuerte entre recursos y corrupción. Sin embargo, la menor eficiencia de recursos en países ricos en ellos sugiere que la dependencia puede inhibir la diversificación económica.
•
Divergencia Regional: La región muestra una creciente disparidad económica, con Kazajistán liderando el crecimiento, mientras que otros países enfrentan desafíos persistentes.
•
Necesidad de Diversificación: La eficiencia de recursos destaca la importancia de diversificar las economías más allá de la extracción para lograr un desarrollo más sostenible y equitativo.
En resumen, si bien los recursos naturales han impulsado el crecimiento en Asia Central, su impacto en la gobernanza y la eficiencia económica es más matizado, sugiriendo que la calidad institucional y las políticas de diversificación son cruciales para un desarrollo integral.