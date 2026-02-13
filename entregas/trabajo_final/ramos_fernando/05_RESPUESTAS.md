# Paso 6: Preguntas de Comprension

**Alumno:** Fernando Ramos

> **Instrucciones:** Responde cada pregunta con tus propias palabras.
> Las respuestas deben ser especificas y demostrar que entiendes los conceptos.
> Se acepta entre 3-5 oraciones por pregunta.
>
> **Nota:** Completa este archivo AL FINAL, despues de haber terminado
> los bloques A, B y C. Asi tendras la experiencia necesaria para responder.

---

## 1. Infraestructura

**Si tu worker tiene 2 GB de RAM y el CSV pesa 3 GB, que pasa?
Como lo solucionarias?**

[Tu respuesta]

Habría un fallo en el worker ya que no tiene suficiente ram para cargar el CSV. 
Desde el compose.yml podrías designar más memoria ram a ese worker para que pudiera manejar el CSV, o crear un nuevo worker con x RAM para procesarlo en paralelo.
---

## 2. ETL

**Por que `spark.read.csv()` no ejecuta nada hasta que llamas
`.count()` o `.show()`?**

[Tu respuesta]

Por el proceceso de Lazy Evaluation que espera a que se llame una accion antes de ejecutar el proceso. Esto permite tener un plan de ejecución optimizado.
## 3. Analisis

**Interpreta tu grafico principal: que patron ves y por que crees
que ocurre?**

En el gráfico principal (scatter de Recursos Naturales vs Control de Corrupción) se observa una correlación débilmente positiva (r=0.208) con mucha dispersión entre los países. El patrón principal es que Kazakhstan, siendo el país con mayor dependencia de recursos (15-25% del PIB), presenta niveles de control de corrupción comparables o superiores a países con poca dependencia como Kyrgyzstan o Tajikistan. Esto contradice la hipótesis clásica de la "maldición de los recursos" y sugiere que la variable determinante no es el volumen de recursos en sí, sino la calidad institucional y la gobernanza en la gestión de las rentas petroleras. Creo que ocurre porque Kazakhstan ha invertido sus ingresos petroleros en construir instituciones más sólidas, mientras que países como Turkmenistan, con alta dependencia pero régimen autoritario, no logran traducir los recursos en mejor gobernanza.

---

## 4. Escalabilidad

**Si tuvieras que repetir este ejercicio con un dataset de 50 GB,
que cambiarias en tu infraestructura?**

Primero, escalaría el clúster de Spark añadiendo más workers en el `docker-compose.yml` (al menos 4-5 workers) y asignando más memoria RAM a cada uno (8-16 GB por worker) para que el procesamiento en paralelo sea efectivo. Segundo, convertiría los datos de origen a formato Parquet particionado por país y año antes de procesarlos, ya que Parquet es columnar y comprimido, lo que reduciría drásticamente el volumen de lectura. Tercero, en lugar de ejecutar el clúster en local, migraría a un entorno cloud (AWS EMR o Google Dataproc) donde puedo escalar horizontalmente los nodos de forma elástica según la carga. Finalmente, aplicaría técnicas de particionamiento (`repartition`) y caché estratégico (`persist`) en las transformaciones intermedias para evitar recálculos innecesarios sobre un dataset tan grande.
