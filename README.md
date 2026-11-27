# TC2008B - Multi-Agents and Computer Graphics project: Modelación de una ciudad

El reto consiste en proponer una solución al problema de movilidad urbana en México, mediante un enfoque que reduzca la congestión vehicular al simular de manera gráfica el tráfico, representando la salida de un sistema multi agentes.

Imagina una solución que implemente una de las siguientes estrategias de ejemplo:

Controlar y asignar los espacios de estacionamiento disponible en una zona de la ciudad, evitando así que los autos estén dando vueltas para encontrar estacionamiento.
Compartir tu vehículo con otras personas. Aumentando la ocupación de los vehículos, reduciría el número de vehículos en las calles.
Tomar las rutas menos congestionadas. Quizás no más las cortas, pero las rutas con menos tráfico. Más movilidad, menos consumo, menos contaminación.
Que permita a los semáforos coordinar sus tiempos y, así, reducir la congestión de un cruce. O, quizás, indicar en qué momento un vehículo va a cruzar una intersección y que de esta forma, el semáforo puede determinar el momento y duración de la luz verde.

Con base en el código de la clase: https://github.com/octavio-navarro/TC2008B
---
## Hecho por:
- Daniela Angulo
- Uriel Anzures

## 📋 Table of Contents

1. [About the Course](#about-the-course)
2. [Repository Structure](#repository-structure)
3. [Prerequisites](#prerequisites)
4. [Installation & Setup](#installation--setup)
5. [References](#references)
6. [License](#license)

---

## Repository Structure

The repository contains the following material:

* **📂 [Documents](./Documents)**
    Contains presentations, cheat sheets, and theoretical resources.
* **📂 [AgentsVisualization](./AgentsVisualization)**
    A WebGL project used to visualize the random agents model using HTML/JS instead of the standard Mesa visualization.
* **📂 [mesaExamples](./mesaExamples)**
    Basic Mesa examples, including the Random Model, Forest Fire, and the City Model.
* **📂 [CompetitionSite](./CompetitionSite)**
    Resources regarding the course competition.

---

## Prerequisites

Before setting up the environment, ensure you have the following installed:

* **Python 3.13+**: [Download Python](https://www.python.org/downloads/)
* **Git**: [Download Git](https://git-scm.com/downloads)

---

## Installation & Setup

We recommend using a Python virtual environment to manage dependencies. This keeps your project isolated from other Python projects on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/octavio-navarro/TC2008B.git
cd TC2008B
````

### 2\. Create the Virtual Environment

Create a virtual environment named `.agents`:

**Windows / macOS / Linux:**

```bash
python -m venv .agents
```

### 3\. Activate the Environment

**Windows (PowerShell):**

```powershell
.\.agents\Scripts\Activate
```

**Windows (Command Prompt):**

```cmd
.\.agents\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .agents/bin/activate
```

*You will know the environment is active when you see `(.agents)` at the start of your command line.*

### 4\. Install Dependencies

Once the environment is active, install the required packages.

**Option A: Using requirements file (Recommended)**

```bash
pip install -r agents_requirements.txt
```

**Option B: Manual Installation**
If you prefer to install the packages manually, run:

```bash
pip install -U "mesa[all]"
pip install flask flask_cors
```

-----

## References

  * **Mesa**: [Official Documentation](https://mesa.readthedocs.io/en/stable/index.html)
  * **Flask**: [User Guide](https://flask.palletsprojects.com/en/3.0.x/)

-----

## License

This project is licensed under the [MIT License](https://www.google.com/search?q=./LICENSE).

