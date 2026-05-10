# Despliegue mínimo

Este despliegue sirve de ejemplo de como una aplicación puede usar la función para la detección de defectos en la madera con la mínima complejidad.

## Instalación

Estos pasos son para ejecutar el ejemplo que se provee dentro del repositorio. Para crear tú propio ejemplo siga los pasos de la documentación principal.

1. Clonar el repositorio

```bash
git clone https://github.com/javizqh/AIVA_2026_maderas.git
cd AIVA_2026_maderas
```

2. Crear un entorno virtual de Python 3.12 o posterior. Si no tiene instalado Python 3.12 o porsterior por favor siga las instrucciones disponibles en https://docs.python.org/3.12/using/index.html. Si la versión de Python instalada de base es >3.12 ejecuta el siguiente comando:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En caso contrario:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

3. Instalar las dependencias de Python.

```bash
pip install -r requirements.txt
```

4. Dirijase al directorio de este ejemplo:

```bash
cd examples/minimum
```

5. Compila tú código fuente enlazando las librerías necesarias (Cambia `python3.12` por la versión instalada posterior a 3.12):

```bash
gcc src/main.c -I/usr/include/python3.12 -I./include -lpython3.12 -o minimum
```

6. Ejecuta el ejemplo

```bash
./minimum
```
