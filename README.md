# TC2008B: Modelación de una ciudad

El reto consiste en proponer una solución al problema de movilidad urbana en México, mediante un enfoque que reduzca la congestión vehicular al simular de manera gráfica el tráfico, representando la salida de un sistema multiagentes.

Imagina una solución que implemente una de las siguientes estrategias de ejemplo:

- Controlar y asignar los espacios de estacionamiento disponibles en una zona de la ciudad, evitando así que los autos estén dando vueltas para encontrar estacionamiento.
- Compartir tu vehículo con otras personas. Al aumentar la ocupación de los vehículos, se reduciría el número de vehículos en las calles.
- Tomar las rutas menos congestionadas. Quizás no las más cortas, pero sí las rutas con menos tráfico. Más movilidad, menos consumo, menos contaminación.
- Que los semáforos coordinen sus tiempos y, así, reduzcan la congestión de un cruce. O, quizás, indicar en qué momento un vehículo va a cruzar una intersección para que el semáforo pueda determinar el momento y la duración de la luz verde.

Con base en el código de la clase: https://github.com/octavio-navarro/TC2008B

---

## Hecho por:
- Daniela Angulo
- Uriel Anzures

## 📋 Contenido

1. [Estructura del repositorio](#estructura-del-repositorio)
2. [Requisitos previos](#requisitos-previos)
3. [Instalación y configuración](#instalación-y-configuración)
4. [Referencias](#referencias)
5. [Licencia](#licencia)

---

## Estructura del repositorio

El repositorio contiene el siguiente material:

* **📂 [mesaExamples/trafficBase](./mesaExamples/trafficBase)**
    Modelo de la ciudad en Mesa (Python): agentes (vehículos, semáforos, calles, edificios y destinos) y mapas de la ciudad en `city_files/`, descritos por `mapDictionary.json`.
* **📂 [AgentsVisualization](./AgentsVisualization)**
    Visualización 3D de la simulación en WebGL.
    * **📂 [Server](./AgentsVisualization/Server)**: servidor en Flask que conecta el modelo de Mesa con WebGL.
    * **📂 [visualization](./AgentsVisualization/visualization)**: página y código del cliente WebGL.
    * **📂 [libs](./AgentsVisualization/libs)**: librerías de matrices, cámara, luces, objetos 3D y carga de modelos OBJ.
    * **📂 [assets](./AgentsVisualization/assets)**: shaders y texturas.

---

## Requisitos previos

Antes de configurar el entorno, asegúrate de tener instalado lo siguiente:

* **Python 3.13+**: [Descargar Python](https://www.python.org/downloads/)
* **Git**: [Descargar Git](https://git-scm.com/downloads)

---

## Instalación y configuración

Recomendamos usar un entorno virtual de Python para manejar las dependencias. Así el proyecto queda aislado de otros proyectos de Python en tu sistema.

### 1. Clonar el repositorio

```bash
git clone https://github.com/0Angulo0/city_project.git
cd city_project
```

### 2. Crear el entorno virtual

Crea un entorno virtual llamado `.agents`:

**Windows / macOS / Linux:**

```bash
python -m venv .agents
```

### 3. Activar el entorno

**Windows (PowerShell):**

```powershell
.\.agents\Scripts\Activate
```

**Windows (Símbolo del sistema / CMD):**

```cmd
.\.agents\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .agents/bin/activate
```

*Sabrás que el entorno está activo cuando veas `(.agents)` al inicio de la línea de comandos.*

### 4. Instalar las dependencias

Con el entorno activo, instala los paquetes necesarios.

**Opción A: Con el archivo de requerimientos (recomendada)**

```bash
pip install -r requirements.txt
```

**Opción B: Instalación manual**

Si prefieres instalar los paquetes a mano, ejecuta:

```bash
pip install -U "mesa[all]"
pip install flask flask_cors
```

---

## Referencias

  * **Mesa**: [Documentación oficial](https://mesa.readthedocs.io/en/stable/index.html)
  * **Flask**: [Guía de usuario](https://flask.palletsprojects.com/en/3.0.x/)

---

## Licencia

Este proyecto está bajo la [Licencia MIT](./LICENSE).
