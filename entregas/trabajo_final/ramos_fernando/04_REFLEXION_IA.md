# Paso 5: Reflexion IA - Proceso de Aprendizaje

**Alumno:** Fernando Ramos

> **Instrucciones:** Para cada bloque (A, B, C), responde 3 preguntas y pega
> el prompt MAS IMPORTANTE que usaste en ese bloque.
>
> Se valoran respuestas **ESPECIFICAS** y **HONESTAS**. No importa si usaste
> IA o no. Lo que importa es que demuestres tu proceso de aprendizaje real.
>
> **Lo que evaluamos:** Tus prompts y tu capacidad de explicar que hiciste.
> Un codigo perfecto con reflexion vacia = nota baja.

---

## Bloque A: Infraestructura Docker

### Momento 1 - Arranque
**Que fue lo primero que le pediste a la IA o buscaste en internet?**

necesito crear un cluster distribuido con Spark y docker. genera un archivo .yml para Tengo un disco SSD externo de 250 GB en el puerto F: de mi ordenador. Mi equipo tiene 16 gb de ram y dos nucleos, quiero crear un maestro y dos trabajadores y mi base de datos esta en esta ruta F:\\LABSTORAGE\\data
     antes de escribir ningun codigo vamos a asegurarnos que esta toda la estructura y todo lo necesario preparado


Entendí que el rol del maestro es coordinar mientras los trabajadores procesan los datos, comunicándose internamente por el puerto 7077 y permitiéndome supervisar todo por el puerto 8080. Para que esto funcione correctamente, la regla depends_on asegura que el coordinador arranque antes que los procesadores. En cuanto a los datos, los volúmenes vinculan las carpetas internas con mi disco físico F:, de manera que la información sequirán ahí aunque el contenedor se detenga. Además, configuraciones como unless-stopped y los healthchecks con pg_isready mantienen el sistema estable y verificado. Sobre la escalabilidad, comprendí que para duplicar la potencia debo crear un nuevo worker y ajustar la memoria y los núcleos tanto en el environment como en el command. Que el puerto 5432 me da acceso externo a la base de datos. Finalmente, domino el ciclo de vida usando docker compose up -d para el segundo plano, ps para verificar el estado y down para limpiar el entorno sin borrar mis archivos físicos en el disco.

### Prompt clave del Bloque A

**Herramienta:** [ChatGPT / Claude / Copilot / otra]

**El prompt que mas te ayudo en este bloque:**
```
me ha dado este error
/opt/entrypoint.sh: line 128: /opt/spark/work-dir/bin/spark-class: No such file or directory
```

**Por que fue clave:** Porque identificó que el problema era la ruta incorrecta del comando spark-class en el docker-compose.yml. Esto hacía que todo lo demás como el healthcheck, volúmenes etc. no funcionara porque Spark simplemente no arrancaba.

## Bloque B: Pipeline ETL

### Momento 1 - Arranque

**Que fue lo primero que le pediste a la IA o buscaste en internet?**

Lo primero que le pedí a la IA fue que me ayudara a crear un script básico de PySpark para leer el archivo CSV qog_std_ts_jan24.csv, filtrar por los 5 países de Asia Central que había seleccionado y seleccionar las columnas de mi análisis. También le pedí que usara rutas relativas para que el proyecto fuera portable.

### Momento 2 - Error

**Que fallo y como lo resolviste?**

El principal problema fue una serie de errores en la configuración de Spark en Windows.
1.
ModuleNotFoundError: No module named 'pyspark': Lo resolvimos creando un entorno virtual (.venv) con Python 3.11 (compatible con Spark) e instalando las dependencias de requirements.txt.
2.
JAVA_HOME environment variable is not set: Lo resolvimos instalando Java (JDK) con winget desde PowerShell.
3.
UnsupportedClassVersionError: El Spark que instalamos requería Java 17, pero yo había instalado Java 11. Lo solucionamos actualizando a Java 17.
4.
HADOOP_HOME and hadoop.home.dir are unset y UnsatisfiedLinkError: Este fue el más difícil. Spark necesita binarios de Hadoop para funcionar en Windows. La solución fue descargar el paquete winutils para la versión correcta de Hadoop (3.3.6), crear una carpeta C:\hadoop\bin y configurar la variable de entorno HADOOP_HOME directamente en el script de Python para asegurar que Spark la encontrara.

### Momento 3 - Aprendizaje

**Que aprendiste que NO sabias antes de empezar este bloque?**

Aprendí que pyspark no es una librería de Python pura, sino una "carcasa" que controla un motor de Java (Spark) que a su vez depende de componentes de otro sistema (Hadoop). No sabía que para usar PySpark en Windows necesitaba tener instalado y configurado no solo Python, sino también el JDK de Java y los binarios de winutils de Hadoop, y que las versiones de todos estos componentes deben ser compatibles entre sí.

### Prompt clave del Bloque B

**Herramienta:** Gemini

**El prompt que mas te ayudo en este bloque:**
```
revisa por favor los .md que estan la arpeta C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\trabajo_final se que en algunoindica que como se han de tratar los vlores nulos
```

**Por que fue clave:** Este prompt fue clave porque, aunque no encontró la respuesta sobre los nulos, me forzó a investigar el contenido real del dataset. Esto nos llevó a descubrir que las columnas que yo había definido en mi README.md (wdi_totalresrent, wdi_gdpcapcon2017) no existían con esos nombres exactos en el CSV. A partir de ahí, pudimos identificar los nombres correctos (wdi_oilrent, wdi_gdpcappppcon2017) y corregir el pipeline para que seleccionara los datos correctos, lo que desbloqueó todo el proceso de transformación posterior.

---

## Bloque C: Analisis y Visualizacion

### Momento 1 - Arranque

**Que fue lo primero que le pediste a la IA o buscaste en internet?**
le pedí que me ayudara a crear un nuevo script (analisis.py) para leer los datos procesados por Spark (el archivo CSV generado) usando la librería pandas. Le pedí que me mostrara cómo cargar los datos y luego cómo usar plotly.express para crear un gráfico de líneas que mostrara la evolución del PIB per cápita (pib_per_capita) a lo largo de los años para cada uno de los cinco países.

### Momento 2 - Error

**Que fallo y como lo resolviste?**

El principal error fue que, al intentar leer el archivo CSV de salida de Spark, el código fallaba porque Spark guarda los resultados en una carpeta (ej. asia_central_processed_csv) que contiene varios archivos (part-00000-...csv, _SUCCESS, etc.), no un único archivo CSV. Mi código inicial intentaba leer la carpeta como si fuera un archivo.
Lo resolvimos pidiéndole a la IA que modificara el código para que buscara automáticamente el primer archivo part-....csv dentro de la carpeta de salida y lo leyera, ignorando los demás.

### Momento 3 - Aprendizaje
**Que aprendiste que NO sabias antes de empezar este bloque?**

Aprendí que la salida de un job de Spark no es un único archivo monolítico, sino una carpeta con múltiples "partes" (una por cada partición del DataFrame en la que trabajó Spark). Esto es una consecuencia directa del procesamiento distribuido. Para leer los resultados con una herramienta no distribuida como pandas, es necesario seleccionar y leer uno de esos archivos part- o concatenarlos todos.

### Prompt clave del Bloque C

**Herramienta:** Gemini

**El prompt que mas te ayudo en este bloque:** *** IMPORTANTE LEER BIEN TODO ANTES DE EJECUTAR NINGUN PASO ***
```
antes de generar el archivo.py tenemos que asegurarnos de que los graficos cumplen con los requisitos adecuados. Los graficos tienen que ser profesionales. Visualmente atractivos, letras de los indices y titulos legibles y sin superponerse. Graficos dinamicos es un punto fuerte, permitir al usuario cambiar entre paises o rangos de tiempo. Para cada grafico propuesto te voy a pasar consejos y ejemplos que he encontrado. Empezamos por los Grafico de regresion:
No es necesario que el eje Y empiece en el valor del "cero"
No utilices colores innecesariamente. Se pueden pintar los puntos para introducir una (3ra) variable categórica al gráfico.
Puedo introducir una 3ra o 4ta variable al gráfico con las siguientes técticas:
Diferentes formas en los "puntos" para introducir una variable categórica.
Convertirlo en un gráfico de burbujas para introducir una variable numérica.
Jugar con la intensidad del color de cada punto para introducir una variable numérica.
Si tengo muy pocos puntos en mi dataset, el resultado del gráfico no será interpretable
Si hay una cantidad grande de puntos en mi dataset, podemos coger una muestra, o jugar con la opacidad de los puntos

**Por que fue clave:** Con este prompt, en vez de solo pedir "un gráfico", le expliqué a la IA cómo quería que se viera y funcionara, como si estuviera dando instrucciones a un diseñador. Le dije qué colores usar, cómo mostrar más datos usando formas o tamaños, y que los gráficos debían ser interactivos. Gracias a esto, el resultado final fue mucho más claro, profesional y me permitió entender mejor la historia que contaban mis datos.

---

## Captura de pantalla

Adjunta UNA captura de pantalla de tu conversacion con la IA mostrando
el prompt que consideras mas significativo de TODO el trabajo.
Si no usaste IA, captura del recurso web/video que mas te sirvio.

![Instrucciones_principales.png](Instrucciones_principales.png)![img.png](img.png)![Mi prompt mas importante](capturas/prompt_clave.png)

Como buena praxis a la hora de trabajar con la IA, es fundamental generar y definir instrucciones previas sobre las que basará todas sus respuestas en todos los prompts que hagamos. En este caso, adjunte en un "espacio" de Claude (en Perplexity) los requisitos principales del proyecto final, incluyendo la base de datos, stack tecnolólogico y físico etc. con el fin de dotar del mayor contexto posible a la IA. Esto marca la diferencia a la hora de recibir sus respuestas.
