# Guía para Alumnos - Cómo Trabajar con los Ejercicios

**Bienvenido al repositorio de ejercicios de Big Data**

Esta guía te enseñará a trabajar correctamente con Git, forks y Pull Requests para entregar tus ejercicios.

---

## 📚 TABLA DE CONTENIDOS

1. [Conceptos Básicos](#conceptos-básicos)
2. [Configuración Inicial](#configuración-inicial)
3. [Flujo de Trabajo Completo](#flujo-de-trabajo-completo)
4. [Best Practices](#best-practices)
5. [Errores Comunes y Cómo Evitarlos](#errores-comunes-y-cómo-evitarlos)
6. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🎯 CONCEPTOS BÁSICOS

### ¿Qué es un Fork?

```
┌───────────────────────────────────────────────────┐
│         REPOSITORIO DEL PROFESOR (Original)       │
│   https://github.com/TodoEconometria/...          │
│                                                    │
│   ├── ejercicios/                                 │
│   ├── datos/                                      │
│   └── README.md                                   │
│                                                    │
│            👇 HACES UN FORK                       │
│                                                    │
│         TU REPOSITORIO (Copia)                    │
│   https://github.com/TU_USUARIO/...               │
│                                                    │
│   ├── ejercicios/  ← Aquí trabajas              │
│   ├── datos/                                      │
│   └── README.md                                   │
│                                                    │
│            👇 HACES UN PULL REQUEST               │
│                                                    │
│         REPOSITORIO DEL PROFESOR                  │
│         (Profesor revisa tu código)               │
└───────────────────────────────────────────────────┘
```

**En resumen:**
- **Fork** = Tu copia personal del repositorio
- **Pull Request (PR)** = Pedir al profesor que revise tu trabajo
- **Commit** = Guardar tus cambios
- **Push** = Subir tus cambios a GitHub

---

## ⚙️ CONFIGURACIÓN INICIAL

### Paso 1: Instalar Git

**Windows:**
```bash
# Descargar e instalar desde: https://git-scm.com/
# O usar winget:
winget install Git.Git
```

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt-get install git  # Ubuntu/Debian
sudo yum install git      # CentOS/Fedora
```

### Paso 2: Configurar Git

```bash
# Configura tu nombre (será visible en los commits)
git config --global user.name "Tu Nombre Completo"

# Configura tu email (usa el mismo que en GitHub)
git config --global user.email "tu@email.com"

# Verifica la configuración
git config --list
```

### Paso 3: Crear Cuenta de GitHub

Si no tienes cuenta:
1. Ir a: https://github.com/
2. Click en "Sign Up"
3. Verificar email

---

## 🔄 FLUJO DE TRABAJO COMPLETO

### PASO 1: Hacer Fork del Repositorio

**Solo haces esto UNA VEZ al inicio del curso**

1. Ir a: https://github.com/TodoEconometria/ejercicios-bigdata
2. Click en el botón **"Fork"** (arriba a la derecha)
3. Seleccionar tu cuenta de GitHub
4. Esperar a que se cree tu fork

✅ Ahora tienes tu propia copia en: `https://github.com/TU_USUARIO/ejercicios-bigdata`

---

### PASO 2: Clonar TU Fork (No el Original)

**¡MUY IMPORTANTE!** Clona TU fork, NO el repositorio del profesor.

```bash
# ❌ MAL - No clones el original:
git clone https://github.com/TodoEconometria/ejercicios-bigdata.git

# ✅ BIEN - Clona TU fork:
git clone https://github.com/TU_USUARIO/ejercicios-bigdata.git

# Entra al directorio
cd ejercicios-bigdata
```

---

### PASO 3: Configurar el Remoto del Profesor (Upstream)

Esto te permite recibir actualizaciones del profesor:

```bash
# Agregar el repositorio del profesor como "upstream"
git remote add upstream https://github.com/TodoEconometria/ejercicios-bigdata.git

# Verificar remotos configurados
git remote -v

# Deberías ver:
# origin    https://github.com/TU_USUARIO/ejercicios-bigdata.git (tu fork)
# upstream  https://github.com/TodoEconometria/ejercicios-bigdata.git (profesor)
```

---

### PASO 4: Trabajar en un Ejercicio

Cada vez que empieces un ejercicio nuevo:

```bash
# 1. Asegúrate de estar en la rama main
git checkout main

# 2. Actualiza tu repositorio con cambios del profesor
git fetch upstream
git merge upstream/main

# 3. Sube las actualizaciones a tu fork
git push origin main

# 4. (OPCIONAL) Crea una rama para el ejercicio
git checkout -b ejercicio-01

# 5. Ve a la carpeta del ejercicio
cd ejercicios/01_nombre_ejercicio/

# 6. Lee el ENUNCIADO.md
cat ENUNCIADO.md

# 7. Si necesitas ayuda, lee AYUDA.md
cat AYUDA.md

# 8. Abre el archivo plantilla_base.py y empieza a trabajar
```

---

### PASO 5: Hacer Commits Frecuentes

**IMPORTANTE:** Haz commits frecuentes mientras trabajas.

```bash
# Ver qué archivos cambiaste
git status

# Ver exactamente qué cambiaste
git diff

# Agregar cambios al staging
git add ejercicios/01_nombre_ejercicio/plantilla_base.py

# O agregar todo:
git add .

# Hacer commit con mensaje descriptivo
git commit -m "Ejercicio 01: Implementar carga de datos CSV"

# Más commits mientras trabajas...
git commit -m "Ejercicio 01: Agregar limpieza de datos"
git commit -m "Ejercicio 01: Implementar análisis estadístico"
git commit -m "Ejercicio 01: Finalizar ejercicio"
```

**Reglas para buenos mensajes de commit:**
- ✅ "Ejercicio 01: Implementar función de carga de datos"
- ✅ "Ejercicio 02: Corregir error en limpieza de outliers"
- ❌ "cambios" (muy vago)
- ❌ "asdfasdf" (sin sentido)
- ❌ "aaaaaa" (inútil)

---

### PASO 6: Subir Cambios a GitHub

```bash
# Subir tus commits a TU fork en GitHub
git push origin main

# O si creaste una rama:
git push origin ejercicio-01
```

---

### PASO 7: Crear Pull Request (PR)

**Cuando termines el ejercicio:**

1. **Ir a GitHub** → Tu fork: `https://github.com/TU_USUARIO/ejercicios-bigdata`

2. **Verás un mensaje amarillo:**
   ```
   "ejercicio-01 had recent pushes"
   [Compare & pull request]
   ```
   Click en "Compare & pull request"

3. **Completar información del PR:**
   ```
   Título: Entrega Ejercicio 01 - [Tu Nombre]

   Descripción:
   ## Ejercicio Completado
   - [x] Ejercicio 01: Análisis de datos NYC Taxi

   ## Qué Hice
   - Cargué los datos CSV
   - Limpié outliers y valores nulos
   - Generé estadísticas descriptivas
   - Creé visualizaciones

   ## Problemas Encontrados
   - Ninguno / [describe si tuviste problemas]

   ## Tiempo Invertido
   - Aproximadamente 3 horas

   ## Comentarios Adicionales
   - [Cualquier cosa que quieras que el profesor sepa]
   ```

4. **Click en "Create Pull Request"**

5. **Esperar revisión del profesor**

---

### PASO 8: Responder a Feedback del Profesor

Si el profesor pide cambios:

```bash
# 1. Hacer los cambios solicitados en tu código local

# 2. Commitear los cambios
git add .
git commit -m "Correcciones según feedback del profesor"

# 3. Subir cambios
git push origin ejercicio-01

# 4. El PR se actualiza automáticamente ✨
```

---

## ✅ BEST PRACTICES

### 1. Commits Frecuentes y Descriptivos

```bash
# ✅ BIEN - Commits pequeños y frecuentes
git commit -m "Agregar función para cargar CSV"
git commit -m "Implementar limpieza de datos nulos"
git commit -m "Agregar validación de tipos de datos"

# ❌ MAL - Un solo commit gigante al final
git commit -m "Todo el ejercicio"
```

**¿Por qué?** Commits pequeños permiten:
- Revertir cambios específicos si algo falla
- Entender la evolución de tu código
- Obtener mejor feedback del profesor

---

### 2. NO Commitear Archivos Innecesarios

**Archivos que NO debes subir:**

```bash
# ❌ NO subir:
.venv/              # Entornos virtuales
__pycache__/        # Cache de Python
*.pyc               # Archivos compilados
.DS_Store           # Archivos de sistema Mac
Thumbs.db           # Archivos de sistema Windows
.idea/              # Configuración de PyCharm
.vscode/            # Configuración de VS Code
*.csv               # Datos grandes (a menos que se indique)
*.db                # Bases de datos locales
```

**El repositorio ya tiene un `.gitignore` configurado, pero verifica antes de hacer commit:**

```bash
# Ver qué archivos subirías
git status

# Si ves archivos que no deberían estar, no los agregues
```

---

### 3. Mantén tu Fork Actualizado

**Cada semana (o antes de empezar un ejercicio nuevo):**

```bash
# Descargar cambios del profesor
git fetch upstream
git checkout main
git merge upstream/main

# Subir actualizaciones a tu fork
git push origin main
```

---

### 4. NO Modifiques Archivos del Repositorio Base

**Solo modifica los archivos del ejercicio específico:**

```bash
# ✅ BIEN - Solo editar archivos del ejercicio
ejercicios/01_nombre_ejercicio/plantilla_base.py
ejercicios/01_nombre_ejercicio/mi_solucion.py

# ❌ MAL - No modificar archivos generales
README.md
.gitignore
requirements.txt
```

**Excepción:** Si encuentras un error en el repositorio, crea un issue en lugar de modificarlo directamente.

---

### 5. Usa Nombres de Branches Descriptivos

```bash
# ✅ BIEN
git checkout -b ejercicio-01
git checkout -b ejercicio-02-limpieza-datos
git checkout -b dashboard-nyc-taxi

# ❌ MAL
git checkout -b test
git checkout -b branch1
git checkout -b aaa
```

---

### 6. Prueba tu Código Antes de Hacer PR

```bash
# Antes de crear el PR, verifica que tu código funcione:

# 1. Ejecuta tu script
python ejercicios/01_nombre_ejercicio/plantilla_base.py

# 2. Verifica que no hay errores

# 3. Lee el ENUNCIADO.md y verifica que cumpliste todos los requisitos

# 4. Si todo funciona, crea el PR
```

---

## 🚨 ERRORES COMUNES Y CÓMO EVITARLOS

### Error 1: Clonar el Repositorio del Profesor en Lugar de tu Fork

```bash
# ❌ ERROR COMÚN
git clone https://github.com/TodoEconometria/ejercicios-bigdata.git
# → No puedes hacer push porque no tienes permisos

# ✅ SOLUCIÓN
# Borra el directorio clonado:
rm -rf ejercicios-bigdata

# Clona TU fork:
git clone https://github.com/TU_USUARIO/ejercicios-bigdata.git
```

---

### Error 2: No Actualizar Fork Antes de Empezar

```bash
# Si no actualizas tu fork, trabajarás con código viejo

# ✅ SIEMPRE HACER ANTES DE EMPEZAR:
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

### Error 3: Hacer Commits de Archivos Grandes

```bash
# Si intentas subir archivos > 100MB, GitHub los rechaza

# ✅ VERIFICAR ANTES DE COMMIT:
git status
# Si ves archivos .csv grandes, NO los agregues

# Si accidentalmente los agregaste:
git reset HEAD archivo_grande.csv
```

---

### Error 4: Trabajar Directamente en `main`

No es un error grave, pero es mejor práctica usar branches:

```bash
# ✅ MEJOR PRÁCTICA
git checkout -b ejercicio-01
# Trabajar...
# Hacer PR desde esta rama

# Si ya trabajaste en main y quieres moverlo a una rama:
git checkout -b ejercicio-01
git push origin ejercicio-01
```

---

### Error 5: No Leer el ENUNCIADO.md Completo

```bash
# ❌ ERROR COMÚN: Empezar a codear sin leer

# ✅ SIEMPRE HACER:
# 1. Leer ENUNCIADO.md COMPLETO
# 2. Leer AYUDA.md si estás atascado
# 3. Entender qué se pide ANTES de codear
# 4. Empezar a trabajar
```

---

### Error 6: Hacer PR Sin Probar el Código

```bash
# ❌ ERROR: Hacer PR con código que no ejecutaste

# ✅ CHECKLIST ANTES DE PR:
□ Ejecuté mi código y funciona sin errores
□ Probé con diferentes datos
□ Leí el ENUNCIADO.md y cumplí todos los requisitos
□ Mi código está comentado cuando es necesario
□ Hice commits descriptivos
□ Ahora sí, crear PR
```

---

### Error 7: Mensajes de Commit Vagos

```bash
# ❌ MAL
git commit -m "cambios"
git commit -m "fix"
git commit -m "update"

# ✅ BIEN
git commit -m "Ejercicio 01: Implementar carga de datos desde CSV"
git commit -m "Ejercicio 01: Agregar función de limpieza de outliers"
git commit -m "Ejercicio 01: Corregir error en cálculo de media"
```

---

## ❓ PREGUNTAS FRECUENTES

### ¿Puedo hacer múltiples PRs a la vez?

Sí, pero usa branches diferentes para cada ejercicio:

```bash
# Ejercicio 1
git checkout -b ejercicio-01
# Trabajar...
git push origin ejercicio-01
# Crear PR desde ejercicio-01

# Ejercicio 2
git checkout main
git checkout -b ejercicio-02
# Trabajar...
git push origin ejercicio-02
# Crear PR desde ejercicio-02
```

---

### ¿Qué hago si el profesor actualiza el repositorio?

```bash
# Actualizar tu fork con cambios del profesor
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Si estás trabajando en una rama:
git checkout ejercicio-01
git merge main  # Integrar cambios en tu rama
```

---

### ¿Puedo colaborar con un compañero?

**Opción 1: Trabajar juntos en un solo fork**
- Uno hace el fork
- Agregar al compañero como colaborador en GitHub
- Ambos clonan el mismo fork

**Opción 2: Cada uno su fork, luego comparar**
- Cada uno trabaja en su fork
- Al terminar, comparan soluciones
- Aprenden de las diferencias

---

### ¿Qué hago si tengo conflictos al hacer merge?

```bash
# Si al hacer git merge upstream/main hay conflictos:

# 1. Git te dirá qué archivos tienen conflicto
git status

# 2. Abrir archivos con conflicto, verás marcadores:
<<<<<<< HEAD
Tu código
=======
Código del profesor
>>>>>>> upstream/main

# 3. Editar manualmente: elige qué código mantener

# 4. Guardar archivo

# 5. Marcar como resuelto:
git add archivo_con_conflicto.py

# 6. Completar el merge:
git commit -m "Resolver conflictos con upstream"
```

---

### ¿Cómo deshago un commit que hice por error?

```bash
# Si NO has hecho push todavía:
git reset HEAD~1  # Deshace último commit, mantiene cambios

# Si YA hiciste push:
git revert HEAD  # Crea un nuevo commit que deshace el anterior
git push origin main
```

---

### ¿Dónde pido ayuda si tengo problemas?

1. **Leer AYUDA.md** del ejercicio
2. **Buscar en Issues** del repositorio: alguien más tuvo el mismo problema
3. **Crear un Issue** usando la plantilla proporcionada
4. **Preguntar en clase** o foros del curso
5. **Revisar documentación oficial** de las librerías que usas

---

## 📝 CHECKLIST RÁPIDA

### Al Inicio del Curso
```
□ Instalé Git
□ Configuré mi nombre y email
□ Creé cuenta de GitHub
□ Hice fork del repositorio del profesor
□ Cloné MI fork (no el original)
□ Agregué upstream (repositorio del profesor)
```

### Antes de Empezar un Ejercicio
```
□ git fetch upstream
□ git merge upstream/main
□ git push origin main
□ Leí ENUNCIADO.md completo
□ Entendí qué se pide
□ (Opcional) Creé branch para el ejercicio
```

### Mientras Trabajo
```
□ Hago commits frecuentes
□ Mensajes de commit descriptivos
□ Pruebo mi código regularmente
□ No subo archivos innecesarios
```

### Antes de Crear PR
```
□ Mi código funciona sin errores
□ Probé con diferentes casos
□ Cumplí todos los requisitos del ENUNCIADO.md
□ Código está comentado donde es necesario
□ Hice push a mi fork
```

### Al Crear PR
```
□ Título descriptivo: "Entrega Ejercicio XX - [Mi Nombre]"
□ Descripción completa
□ Mencioné problemas encontrados (si los hubo)
□ Mencioné tiempo invertido
```

---

## 🎓 RECURSOS ADICIONALES

### Documentación Git
- [Git - La guía sencilla](https://rogerdudler.github.io/git-guide/index.es.html)
- [Pro Git Book (Español)](https://git-scm.com/book/es/v2)
- [GitHub Guides](https://guides.github.com/)

### Tutoriales Interactivos
- [Learn Git Branching](https://learngitbranching.js.org/?locale=es_ES)
- [GitHub Learning Lab](https://lab.github.com/)

### Comandos Git de Referencia
```bash
# Estado y cambios
git status                  # Ver estado
git diff                    # Ver cambios no commiteados
git log --oneline -10       # Ver últimos 10 commits

# Branches
git branch                  # Ver branches
git checkout -b nombre      # Crear y cambiar a branch
git checkout main           # Volver a main

# Sincronización
git fetch upstream          # Descargar cambios del profesor
git merge upstream/main     # Integrar cambios
git push origin main        # Subir a tu fork

# Commits
git add .                   # Agregar todos los cambios
git commit -m "mensaje"     # Hacer commit
git push                    # Subir commits
```

---

## 💪 ¡Éxito en tus Ejercicios!

Recuerda:
- **Lee las instrucciones completas** antes de empezar
- **Haz commits frecuentes** con mensajes descriptivos
- **Prueba tu código** antes de crear PR
- **Pide ayuda** cuando la necesites
- **Aprende de los errores** - son parte del proceso

**¡Buena suerte!** 🚀
