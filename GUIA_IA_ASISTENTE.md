# Guía de Uso de Inteligencia Artificial como Asistente de Programación

> La IA es una herramienta poderosa para aprender. Úsala como un tutor, no como un copiador de tareas.

## ¿Qué es la IA para Programación?

La Inteligencia Artificial puede ayudarte a:
- **Entender código** que no comprendes
- **Encontrar errores** en tu código
- **Aprender conceptos** con explicaciones personalizadas
- **Generar código** de ejemplo para aprender
- **Traducir errores** técnicos a lenguaje simple

**Lo que NO debe hacer**:
- ❌ Hacer toda la tarea por ti
- ❌ Ser tu única fuente de aprendizaje
- ❌ Reemplazar tu razonamiento crítico

## Herramientas de IA Disponibles

### 1. Google Gemini (RECOMENDADO)

**¿Qué es?** El asistente de IA de Google, completamente gratuito y muy potente para programación.

**Cómo usarlo**:
1. Ve a [gemini.google.com](https://gemini.google.com)
2. Inicia sesión con tu cuenta de Google (Gmail)
3. ¡Ya está! Comienza a hacer preguntas

**Ventajas**:
- ✅ Totalmente gratuito
- ✅ No requiere registro especial (usa tu Gmail)
- ✅ Excelente para código Python y Big Data
- ✅ Puede analizar imágenes (útil si capturas errores)
- ✅ Integración con Google Colab

**Ejemplo de uso**:
```
Tú: "Estoy en el ejercicio 01_cargar_sqlite.py línea 23.
     Explícame qué hace esta línea: engine = create_engine('sqlite:///taxi.db')"

Gemini: "Esta línea crea una conexión a una base de datos SQLite.
        - create_engine: función de SQLAlchemy para conectarse a bases de datos
        - 'sqlite:///': indica que es una base SQLite (3 barras = archivo local)
        - taxi.db: nombre del archivo de base de datos

        Es como abrir un canal de comunicación con tu base de datos para poder
        consultar y manipular los datos almacenados en ella."
```

### 2. Claude Code (Claude AI)

**¿Qué es?** Un asistente de IA de Anthropic especializado en código y explicaciones técnicas.

**Cómo usarlo**:
1. Ve a [claude.ai](https://claude.ai) o usa la extensión de VS Code
2. Crea una cuenta gratuita
3. Haz preguntas sobre el código

**Ventajas**:
- ✅ Muy bueno para explicaciones detalladas
- ✅ Extensión de VS Code disponible
- ✅ Excelente para razonamiento complejo

### 3. ChatGPT

**¿Qué es?** Chatbot de OpenAI para preguntas generales y explicaciones.

**Cómo usarlo**:
1. Ve a [chat.openai.com](https://chat.openai.com)
2. Crea una cuenta gratuita
3. Haz preguntas

**Mejor para**: Conceptos generales, errores, explicaciones de Python básico.

### 4. GitHub Copilot

**¿Qué es?** Autocompleta código mientras escribes (como el autocompletado de Gmail, pero para código).

**Cómo activarlo** (requiere subscripción de estudiante gratuita):
1. Aplica a [GitHub Student Developer Pack](https://education.github.com/pack)
2. Instala la extensión en VS Code o PyCharm
3. Escribe comentarios y te sugiere código

**Ejemplo**:
```python
# Cargar datos de un archivo CSV en un DataFrame de pandas
# Copilot sugiere automáticamente:
import pandas as pd
df = pd.read_csv('datos.csv')
```

### 5. Otras Herramientas

| Herramienta | Uso | Gratuita |
|-------------|-----|----------|
| **Phind** | Búsqueda técnica con IA | ✅ Sí |
| **Cursor AI** | Editor de código con IA integrada | ⚠️ Prueba gratis |
| **CodeWhisperer** (Amazon) | Autocompletado (competencia de Copilot) | ✅ Sí |
| **Perplexity AI** | Búsqueda con referencias | ✅ Sí |

## Comparativa Rápida: ¿Cuál Usar?

| Situación | Herramienta Recomendada |
|-----------|------------------------|
| **Primera vez con IA** | 🥇 **Gemini** (más fácil, usa tu Gmail) |
| **Explicaciones detalladas** | Claude o Gemini |
| **Autocompletado mientras escribes** | GitHub Copilot |
| **Búsqueda técnica con fuentes** | Perplexity o Phind |
| **Análisis de imágenes de errores** | Gemini (acepta capturas de pantalla) |
| **Uso académico general** | Gemini o ChatGPT |

## Cómo Hacer Buenas Preguntas a la IA

### ❌ Pregunta Mala
```
"Me da error"
```

### ✅ Pregunta Buena
```
Estoy ejecutando el ejercicio 01_cargar_sqlite.py y me sale este error:

FileNotFoundError: [Errno 2] No such file or directory: 'taxi.db'

El código en la línea 23 es:
engine = create_engine('sqlite:///taxi.db')

¿Qué significa este error y cómo lo soluciono?
```

**¿Por qué es mejor?**
- Contexto específico (qué ejercicio)
- Error completo
- Código relevante
- Pregunta clara

## Estrategias de Aprendizaje con IA

### Estrategia 1: El Método "Explícamelo como a un niño"

```
Tú: "Explícame qué es un DataFrame de pandas como si tuviera 10 años"

IA: "Un DataFrame es como una hoja de cálculo de Excel, pero dentro de Python.
     Tiene filas (como las líneas en Excel) y columnas (como las letras A, B, C...).
     Cada columna tiene un nombre, como 'nombre', 'edad', 'ciudad'..."
```

### Estrategia 2: El Método "Paso a Paso"

```
Tú: "Explica esta línea de código paso por paso:
     df.groupby('VendorID')['total_amount'].mean()"

IA: "Vamos paso por paso:
     1. df.groupby('VendorID'): Agrupa las filas por el valor de VendorID
     2. ['total_amount']: Selecciona solo la columna total_amount
     3. .mean(): Calcula el promedio de cada grupo

     Resultado: El promedio de total_amount para cada VendorID"
```

### Estrategia 3: El Método "Debugging Guiado"

```
Tú: "Mi código debería mostrar 10 filas pero muestra 5. Aquí está mi código:
     [pega tu código]
     ¿Dónde puede estar el problema?"

IA: "Veo el problema en la línea 15:
     df.head(5)

     El método .head(5) muestra solo las primeras 5 filas.
     Cambia el 5 por 10:
     df.head(10)"
```

### Estrategia 4: El Método "Verificación"

```
Tú: "Escribí este código para cargar datos. ¿Está correcto o tiene errores?
     [pega tu código]"

IA: "Tu código funciona, pero tiene un par de mejoras posibles:
     1. Falta manejo de errores si el archivo no existe
     2. Podrías especificar el tipo de datos (dtype) para mejor rendimiento..."
```

## Uso Ético de la IA

### ✅ Uso Correcto
- **Entender un error** que no comprendes
- **Pedir explicaciones** de código que leíste
- **Verificar** si tu solución es correcta
- **Aprender** conceptos nuevos con ejemplos
- **Depurar** código que escribiste tú mismo

### ❌ Uso Incorrecto
- Copiar código sin entenderlo
- Hacer que la IA resuelva todo el ejercicio
- No leer las explicaciones
- Depender 100% de la IA sin intentar primero
- Entregar código generado sin modificar

## El Método de los 3 Intentos

Antes de usar IA, sigue esta regla:

1. **Intento 1**: Intenta resolverlo tú mismo (10-15 minutos)
2. **Intento 2**: Busca en Google o documentación (10 minutos)
3. **Intento 3**: Ahora sí, pregunta a la IA

**¿Por qué?**
- Desarrollas habilidades de resolución de problemas
- Aprendes a buscar información (habilidad crucial)
- Valoras más la ayuda de la IA

## Prompts Útiles para este Curso

### Para Entender Conceptos
```
"Explica qué es [concepto] en el contexto de Big Data y Python.
 Dame un ejemplo práctico aplicado a datos de taxis."
```

### Para Depurar
```
"Tengo este error: [pega el error completo]
 En el archivo: [nombre del archivo]
 En esta línea: [número de línea y código]
 ¿Qué significa y cómo lo arreglo?"
```

### Para Aprender
```
"Estoy aprendiendo [tema, ej. Pandas].
 Dame 3 ejemplos prácticos de cómo usar [función]
 con datos similares a los de este ejercicio."
```

### Para Revisar
```
"Aquí está mi solución al ejercicio [número]:
 [pega tu código]

 ¿Está correcto? ¿Qué podría mejorar?
 ¿Hay errores que no veo?"
```

### Para Comparar
```
"Resolví este problema de dos formas diferentes.
 ¿Cuál es mejor y por qué?

 Opción 1: [código]
 Opción 2: [código]"
```

## Limitaciones de la IA

La IA puede:
- ❌ Dar información desactualizada
- ❌ Inventar funciones que no existen
- ❌ Confundirse con contexto complejo
- ❌ No entender tu entorno específico

**Solución**: Siempre verifica lo que te dice la IA:
- Ejecuta el código que te da
- Busca en la documentación oficial
- Pregunta a tu profesor si tienes dudas

## Configuración y Primeros Pasos

### Empezar con Gemini (RECOMENDADO para principiantes)

1. **Abre tu navegador** y ve a [gemini.google.com](https://gemini.google.com)
2. **Inicia sesión** con tu cuenta de Gmail
3. **Prueba tu primera pregunta**:
   ```
   "Hola, estoy aprendiendo Python y Big Data.
    ¿Puedes explicarme qué es un DataFrame?"
   ```
4. **¡Listo!** Ya puedes usar Gemini

**Tips para Gemini**:
- Puedes subir imágenes (capturas de pantalla de errores)
- Mantiene el historial de conversaciones
- Puedes compartir conversaciones con tu profesor
- Funciona en español e inglés

### Configuración de Claude Code en VS Code (Opcional)

1. Abre VS Code
2. Ve a Extensions (Ctrl+Shift+X)
3. Busca "Claude Code" o "Anthropic"
4. Instala la extensión
5. Inicia sesión con tu cuenta de Claude

**Atajos útiles**:
- `Ctrl+Shift+P` → "Ask Claude": Pregunta directa
- Selecciona código → Click derecho → "Explain with Claude"

### Configuración de GitHub Copilot (Opcional)

1. Aplica al [GitHub Student Pack](https://education.github.com/pack)
2. Una vez aprobado (puede tardar unos días)
3. Instala la extensión de Copilot en tu editor
4. Inicia sesión con tu cuenta de GitHub
5. Escribe comentarios y te autocompleta

## Ejercicio Práctico: Tu Primera Conversación con IA

**Abre Gemini ahora** ([gemini.google.com](https://gemini.google.com)) y prueba estos prompts:

### 1. Nivel Básico - Conceptos
```
"Hola Gemini, estoy comenzando a aprender Python para Big Data.
¿Puedes explicarme la diferencia entre una lista y un DataFrame en Python?
Dame ejemplos prácticos."
```

### 2. Nivel Intermedio - Código Específico
```
"Tengo un DataFrame de pandas con estas columnas: fecha, ciudad, temperatura.
¿Puedes mostrarme el código para calcular la temperatura promedio por ciudad?
Explica cada línea del código."
```

### 3. Nivel Avanzado - Conceptos Técnicos
```
"Estoy estudiando Dask para Big Data.
¿Puedes explicar qué es 'lazy evaluation' y por qué es importante?
Usa un ejemplo aplicado a un dataset de taxis de NYC."
```

### 4. Debugging - Tu Primer Error (Prueba esto cuando tengas un error real)
```
"Gemini, estoy ejecutando este código Python:
[pega tu código aquí]

Y me sale este error:
[pega el error completo aquí]

¿Qué significa este error y cómo lo soluciono?"
```

## Checklist de Uso Responsable

Antes de preguntar a la IA:
- [ ] ¿Intenté resolverlo yo mismo?
- [ ] ¿Busqué en Google/documentación?
- [ ] ¿Mi pregunta es específica y clara?
- [ ] ¿Incluí el error completo si hay uno?
- [ ] ¿Incluí el código relevante?

Después de recibir la respuesta:
- [ ] ¿Entiendo la explicación?
- [ ] ¿Probé el código que me dio?
- [ ] ¿Busqué verificar la información?
- [ ] ¿Agregué comentarios con MI entendimiento?
- [ ] ¿Podría explicar esto a otra persona?

## Recursos Adicionales

### Herramientas de IA
- [Google Gemini](https://gemini.google.com) - Empieza aquí (gratis)
- [ChatGPT](https://chat.openai.com) - Alternativa popular (gratis)
- [Claude AI](https://claude.ai) - Explicaciones detalladas (gratis)
- [GitHub Copilot](https://github.com/features/copilot) - Autocompletado en VS Code

### Tutoriales y Cursos
- [Prompts efectivos para código](https://www.youtube.com/results?search_query=effective+prompts+for+coding+AI)
- [Curso: IA para Desarrolladores](https://www.deeplearning.ai/short-courses/)
- [Google AI Essentials](https://grow.google/ai-essentials/) - Curso gratuito de Google
- [Guía de GitHub Copilot](https://docs.github.com/en/copilot)

## Reflexión Final

La IA es como una calculadora:
- Una calculadora te ayuda con operaciones complejas ✅
- Pero necesitas entender matemáticas ✅
- No puedes depender solo de ella ✅

De la misma forma:
- La IA te ayuda con código complejo ✅
- Pero necesitas entender programación ✅
- No puedes depender solo de ella ✅

**Tu objetivo**: Aprender a programar, no aprender a copiar de la IA.

---

**¿Listo para empezar?** Abre [Gemini](https://gemini.google.com) ahora mismo y haz tu primera pregunta sobre Big Data y Python.

---

## Resumen: Tu Plan de Acción

1. ✅ **Abre Gemini** → [gemini.google.com](https://gemini.google.com)
2. ✅ **Inicia sesión** con tu Gmail
3. ✅ **Haz tu primera pregunta** de prueba
4. ✅ **Guarda el enlace** en tus marcadores
5. ✅ **Úsalo durante los ejercicios** siguiendo el método de los 3 intentos

**Recuerda**: La IA es tu asistente de aprendizaje, no tu reemplazo. Úsala para entender, no para copiar.

> "La IA no reemplaza tu cerebro, lo potencia. Úsala sabiamente."
