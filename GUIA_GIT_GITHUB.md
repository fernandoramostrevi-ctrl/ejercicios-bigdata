# Guía Completa de Git y GitHub para Principiantes

> Esta guía te enseñará desde cero cómo usar Git y GitHub. No necesitas experiencia previa.

## ¿Qué es Git y para qué sirve?

Imagina que estás escribiendo un ensayo importante. Guardas versiones con nombres como:
- `ensayo_final.docx`
- `ensayo_final_REAL.docx`
- `ensayo_final_AHORA_SI.docx`
- `ensayo_final_DEFINITIVO_v3.docx`

**Git** es un sistema que guarda automáticamente todas las versiones de tu trabajo de forma organizada. Te permite:
- Volver a cualquier versión anterior
- Ver qué cambió y cuándo
- Trabajar en equipo sin que se pisen el código
- Experimentar sin miedo a romper nada

## ¿Qué es GitHub?

**GitHub** es como Google Drive o Dropbox, pero especializado para código:
- Guardas tu código en la nube
- Compartes proyectos con otros
- Otros pueden ver tu trabajo (¡es tu portafolio!)
- Tu profesor puede ver tu progreso

## Conceptos Básicos (Diccionario)

| Término | Significado Simple | Ejemplo |
|---------|-------------------|---------|
| **Repositorio (repo)** | Una carpeta de proyecto con historial | Este proyecto de ejercicios |
| **Fork** | Tu copia personal de un repo de otra persona | Tu copia de este proyecto |
| **Clone** | Descargar un repositorio a tu computadora | Bajar tu fork a tu PC |
| **Commit** | Guardar un punto en la historia | "Terminé el ejercicio 1" |
| **Push** | Subir tus cambios a GitHub | Enviar tu progreso a la nube |
| **Pull** | Descargar cambios desde GitHub | Traer actualizaciones |

## Instalación de Git

### Windows
1. Descarga Git desde: https://git-scm.com/download/win
2. Ejecuta el instalador (siguiente, siguiente, siguiente...)
3. Deja todas las opciones por defecto

### Mac
Abre la Terminal y escribe:
```bash
git --version
```
Si no está instalado, macOS te pedirá instalarlo automáticamente.

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

### Verificar la instalación
Abre una terminal (Command Prompt en Windows o Terminal en Mac/Linux) y escribe:
```bash
git --version
```
Deberías ver algo como: `git version 2.x.x`

## Configuración Inicial (Solo una vez)

Dile a Git quién eres:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

**IMPORTANTE**: Usa el mismo email que usaste en GitHub.

## Paso a Paso: Trabajando con este Proyecto

### Paso 1: Haz un Fork (En GitHub.com)

1. Ve al repositorio original en GitHub
2. Haz clic en el botón **"Fork"** (arriba a la derecha)
3. Selecciona tu cuenta personal
4. Espera unos segundos

¡Felicidades! Ahora tienes tu propia copia del proyecto en `https://github.com/TU_USUARIO/ejercicios_bigdata`

**¿Por qué Fork y no Clone directo?**
- Un fork te da tu propia copia donde puedes experimentar libremente
- Tu profesor puede ver todos los forks y su progreso
- El repositorio original no se contamina con tu código

### Paso 2: Clona TU Fork a tu Computadora

Abre tu terminal y navega a donde quieres guardar el proyecto:

```bash
# Ir a tu carpeta de documentos (ejemplo)
cd Documents

# Clonar TU fork (reemplaza TU_USUARIO)
git clone https://github.com/TU_USUARIO/ejercicios_bigdata.git

# Entrar a la carpeta del proyecto
cd ejercicios_bigdata
```

### Paso 3: Trabaja en los Ejercicios

1. Abre el proyecto en tu editor favorito (VS Code, PyCharm, etc.)
2. Lee las instrucciones en `LEEME.md`
3. Trabaja en los ejercicios
4. Modifica archivos, prueba código

### Paso 4: Revisa tus Cambios

```bash
# Ver qué archivos modificaste
git status
```

Verás algo como:
```
modified:   ejercicios/01_cargar_sqlite.py
modified:   PROGRESO.md
```

### Paso 5: Guarda tus Cambios (Commit)

Un **commit** es como tomar una foto del estado actual de tu proyecto.

```bash
# Agregar archivos específicos
git add ejercicios/01_cargar_sqlite.py
git add PROGRESO.md

# O agregar todos los archivos modificados
git add .

# Guardar con un mensaje descriptivo
git commit -m "Completé el ejercicio 1 de SQLite"
```

**Buenos mensajes de commit**:
- ✅ "Completé ejercicio 1 de SQLite"
- ✅ "Arreglé error en limpieza de datos"
- ✅ "Agregué comentarios al código de Dask"

**Malos mensajes**:
- ❌ "cambios"
- ❌ "asdf"
- ❌ "cosas"

### Paso 6: Sube tus Cambios a GitHub (Push)

```bash
git push origin main
```

Si es tu primera vez, Git te pedirá tu usuario y contraseña de GitHub.

**¿Qué significa esto?**
- `push`: Subir
- `origin`: Tu fork en GitHub
- `main`: La rama principal (no te preocupes por esto ahora)

### Paso 7: Verifica en GitHub

1. Ve a tu fork en GitHub: `https://github.com/TU_USUARIO/ejercicios_bigdata`
2. Deberías ver tus cambios reflejados
3. Tu profesor puede ver tu progreso visitando tu fork

## Flujo de Trabajo Diario

Este será tu ciclo normal de trabajo:

```bash
# 1. Trabaja en tu código
# (edita archivos, prueba, experimenta)

# 2. Revisa qué cambiaste
git status

# 3. Guarda tus cambios
git add .
git commit -m "Descripción clara de lo que hiciste"

# 4. Sube a GitHub
git push origin main
```

**Repite este ciclo varias veces al día**. No esperes a terminar todo para hacer commit.

## Comandos Útiles

### Ver el historial de commits
```bash
git log

# Versión más compacta
git log --oneline
```

### Ver diferencias antes de commit
```bash
# Ver qué cambió en cada archivo
git diff
```

### Deshacer cambios (antes de commit)
```bash
# Descartar cambios en un archivo específico
git checkout -- nombre_archivo.py

# Descartar TODOS los cambios no guardados (¡cuidado!)
git reset --hard
```

### Actualizar tu fork con cambios del profesor
```bash
# Solo una vez: agregar el repo original como "upstream"
git remote add upstream https://github.com/PROFESOR_USUARIO/ejercicios_bigdata.git

# Descargar cambios del profesor
git fetch upstream

# Fusionar cambios en tu proyecto
git merge upstream/main
```

## Problemas Comunes y Soluciones

### "No puedo hacer push"
**Problema**: `error: failed to push some refs`

**Solución**:
```bash
# Primero descarga cambios de GitHub
git pull origin main

# Luego intenta push de nuevo
git push origin main
```

### "Modifiqué algo por error"
**Solución**:
```bash
# Ver el historial
git log --oneline

# Volver a un commit anterior (reemplaza CODIGO por el hash del commit)
git reset --hard CODIGO_DEL_COMMIT
```

### "Se me olvidó agregar un archivo al commit"
```bash
# Agrega el archivo
git add archivo_olvidado.py

# Añádelo al último commit
git commit --amend --no-edit
```

### "Cambié de computadora"
```bash
# En la nueva computadora, clona tu fork
git clone https://github.com/TU_USUARIO/ejercicios_bigdata.git
cd ejercicios_bigdata

# Continúa trabajando normalmente
```

## Buenas Prácticas

1. **Haz commits frecuentes**: Cada vez que termines una tarea pequeña
2. **Mensajes descriptivos**: Que se entienda qué hiciste
3. **Push al menos 1 vez al día**: Así tu trabajo está respaldado
4. **No hagas commit de archivos grandes**: Datos, bases de datos (ya está en `.gitignore`)
5. **Lee los errores**: Git te dice qué salió mal

## Glosario Visual

```
TU COMPUTADORA                    GITHUB (Nube)
═══════════════                   ══════════════

[Archivos editados]
       ↓
   git add
       ↓
[Staging Area]
       ↓
   git commit
       ↓
[Repositorio Local] -----------> [Tu Fork]
                    git push
                                     ↓
                                 (Tu profesor
                                  ve tu fork)
```

## Recursos para Aprender Más

- **Interactivo**: [Learn Git Branching](https://learngitbranching.js.org/?locale=es_ES) (juego visual)
- **Video**: Busca "git y github para principiantes" en YouTube
- **Documentación**: [Git Book en Español](https://git-scm.com/book/es/v2)
- **Cheat Sheet**: [Comandos Git más usados](https://training.github.com/downloads/es_ES/github-git-cheat-sheet/)

## Próximos Pasos

1. ✅ Lee esta guía completamente
2. ✅ Instala Git en tu computadora
3. ✅ Configura tu nombre y email
4. ✅ Haz fork de este proyecto
5. ✅ Clona tu fork
6. ✅ Haz tu primer commit
7. ✅ Haz push a GitHub
8. ✅ Verifica en GitHub que se subió

---

**¡Felicidades!** Ya sabes lo básico de Git y GitHub. Con la práctica te volverás un experto.

> "El mejor momento para aprender Git fue ayer. El segundo mejor momento es ahora."
