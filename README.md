# Ejercicios Prácticos de Big Data con Python

> **Para estudiantes**: Este es tu espacio de aprendizaje. Aquí aprenderás Big Data desde cero, trabajando con datos reales y herramientas profesionales.

## Bienvenida

¡Felicidades por comenzar tu viaje en el mundo del Big Data! Este repositorio contiene ejercicios prácticos diseñados para que aprendas haciendo. No necesitas experiencia previa en programación ni en Git/GitHub.

## ¿Qué aprenderás?

- **Python para Datos**: Manipulación de datos con Pandas
- **Bases de Datos**: SQL con SQLite
- **Big Data**: Procesamiento con Dask y Apache Spark
- **Formatos Modernos**: Trabajo con archivos Parquet
- **Git & GitHub**: Control de versiones (¡tu primera vez!)
- **IA como Asistente**: Uso de herramientas de IA para programar

## Antes de Empezar

### Paso 1: Haz un Fork de este Repositorio

Un **fork** es tu copia personal de este proyecto donde trabajarás sin afectar el original.

1. Haz clic en el botón **Fork** (arriba a la derecha en GitHub)
2. Selecciona tu cuenta personal
3. ¡Listo! Ahora tienes tu propia copia

### Paso 2: Configura tu Proyecto

**IMPORTANTE**: Sigue las instrucciones completas en:
### 👉 **[INSTRUCCIONES_CONFIGURACION.md](./INSTRUCCIONES_CONFIGURACION.md)** 👈

Este archivo te guiará paso a paso para:
- Clonar el repositorio
- Crear las carpetas de trabajo
- Copiar las plantillas de ejercicios
- Instalar Python y dependencias
- Descargar los datos

### Paso 3: Lee las Guías

Este repositorio incluye guías para ayudarte:

- **[INSTRUCCIONES_CONFIGURACION.md](./INSTRUCCIONES_CONFIGURACION.md)**: Configuración inicial (¡empieza aquí!)
- **[GUIA_GIT_GITHUB.md](./GUIA_GIT_GITHUB.md)**: Todo sobre Git y GitHub
- **[GUIA_IA_ASISTENTE.md](./GUIA_IA_ASISTENTE.md)**: Cómo usar IA para aprender (Gemini, Claude, ChatGPT)
- **[LEEME.md](./LEEME.md)**: Instrucciones técnicas de los ejercicios
- **[ARQUITECTURA_Y_STACK.md](./ARQUITECTURA_Y_STACK.md)**: Conceptos avanzados (opcional)

### Paso 4: Prepara tu Entorno

Necesitarás:
- **Python 3.8+** instalado ([Descargar aquí](https://www.python.org/downloads/))
- **Git** instalado ([Descargar aquí](https://git-scm.com/downloads))
- Un editor de código (recomendamos [VS Code](https://code.visualstudio.com/) o PyCharm)

## Estructura del Proyecto

```
ejercicios_bigdata/
├── README.md                       # Este archivo
├── INSTRUCCIONES_CONFIGURACION.md  # Configuración inicial (¡LEE ESTO PRIMERO!)
├── GUIA_GIT_GITHUB.md              # Guía de Git para principiantes
├── GUIA_IA_ASISTENTE.md            # Guía para usar IA (Gemini, Claude, ChatGPT)
├── LEEME.md                        # Instrucciones técnicas de ejercicios
├── ARQUITECTURA_Y_STACK.md         # Conceptos técnicos
├── requirements.txt                # Librerías Python necesarias
├── PROGRESO.md                     # Tu checklist de avance
├── plantillas/                     # Plantillas originales (NO modificar)
│   ├── datos/
│   │   └── descargar_datos.py      # Plantilla del script de descarga
│   └── ejercicios/
│       ├── 01_cargar_sqlite.py     # Plantilla ejercicio 1
│       ├── 02_limpieza_datos.py    # Plantilla ejercicio 2
│       ├── 03_parquet_dask.py      # Plantilla ejercicio 3
│       └── 04_pyspark_query.py     # Plantilla ejercicio 4
├── datos/                          # TU carpeta (crearás después)
│   └── descargar_datos.py          # Tu copia para trabajar
└── ejercicios/                     # TU carpeta (crearás después)
    ├── 01_cargar_sqlite.py         # Tu ejercicio 1
    ├── 02_limpieza_datos.py        # Tu ejercicio 2
    ├── 03_parquet_dask.py          # Tu ejercicio 3
    └── 04_pyspark_query.py         # Tu ejercicio 4
```

**Nota**: Las carpetas `datos/` y `ejercicios/` NO están en el repositorio inicial. Las crearás siguiendo **[INSTRUCCIONES_CONFIGURACION.md](./INSTRUCCIONES_CONFIGURACION.md)**.

## Cómo Trabajar en este Proyecto

### Sigue este Orden:

1. **Lee** → [INSTRUCCIONES_CONFIGURACION.md](./INSTRUCCIONES_CONFIGURACION.md) (configuración completa)
2. **Lee** → [GUIA_GIT_GITHUB.md](./GUIA_GIT_GITHUB.md) (si no conoces Git)
3. **Lee** → [GUIA_IA_ASISTENTE.md](./GUIA_IA_ASISTENTE.md) (cómo usar Gemini y otras IAs)
4. **Lee** → [LEEME.md](./LEEME.md) (instrucciones de ejercicios)
5. **Comienza** → Ejercicio 01_cargar_sqlite.py
6. **Actualiza** → PROGRESO.md después de cada ejercicio
7. **Haz commit y push** → Sube tu progreso a GitHub regularmente

## Seguimiento de tu Progreso

1. Abre el archivo [PROGRESO.md](./PROGRESO.md)
2. Marca ✅ cada ejercicio que completes
3. Haz commit de tus cambios regularmente
4. Sube (push) tus commits a GitHub

Tu profesor podrá ver tu progreso en tu fork.

## Cómo Pedir Ayuda

### Opción 1: Usa IA como Asistente
Lee la [GUIA_IA_ASISTENTE.md](./GUIA_IA_ASISTENTE.md) para aprender a pedir ayuda a herramientas como:
- Claude Code
- GitHub Copilot
- ChatGPT

### Opción 2: Abre un Issue
Si tienes problemas:
1. Ve a la pestaña "Issues" en tu fork
2. Crea un nuevo issue describiendo el problema
3. Comparte el enlace con tu profesor

### Opción 3: Pregunta a tu Profesor
Comparte el enlace de tu fork con tu profesor para que vea tu código.

## Reglas de Oro

1. **No tengas miedo de equivocarte**: Los errores son parte del aprendizaje
2. **Haz commits frecuentes**: Guarda tu progreso regularmente
3. **Lee los comentarios del código**: Ahí está la explicación
4. **Usa la IA con criterio**: Úsala para entender, no solo para copiar
5. **Pide ayuda cuando la necesites**: Nadie nace sabiendo

## Recursos Adicionales

- [Documentación oficial de Python](https://docs.python.org/es/)
- [Documentación de Pandas](https://pandas.pydata.org/docs/)
- [Tutorial interactivo de Git](https://learngitbranching.js.org/?locale=es_ES)
- [Curso gratuito de Big Data (YouTube)](https://www.youtube.com/results?search_query=big+data+python+tutorial+español)

## Licencia

Este material es de uso educativo. Siéntete libre de aprender y compartir.

---

**¡Éxito en tu aprendizaje!** Recuerda: todos los profesionales fueron principiantes alguna vez.
