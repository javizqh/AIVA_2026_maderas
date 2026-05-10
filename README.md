[![Deploy and test the application in an enviroment similar to production](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/deploy_test.yml/badge.svg?branch=main)](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/deploy_test.yml)
[![Python Linting](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/python_lint.yml/badge.svg?branch=main)](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/python_lint.yml)

# AIVA_2026_maderas

El proyecto consiste en el desarrollo de un sistema de visión artificial para detectar defectos en tablas de madera. La juguetera artesanal crea piezas de madera a partir de tablas y quiere descartar defectos de dichas tablas para que no estén presentes en las piezas. Con este objetivo se pretende implementar el sistema software en una línea de producción para cribar los defectos. El sistema final será capaz de detectar defectos, localizarlos y proporcionar una medida de la confianza de la detección de los defectos presentes en una tabla de madera. La localización será proporcionada con un bounding box que engloba el defecto, y el factor de confianza con un valor de 0 a 1. Las salidas del sistema serán almacenadas en un archivo XML.

## Guia de instalación

Para poder usar este proyecto tanto en Python como en C es necesario seguir los siguientes pasos para cada uno de ellos, pero primero es necesario clonar el repositorio con el siguiente comando:

```bash
git clone https://github.com/javizqh/AIVA_2026_maderas.git
```

El segundo paso consiste en crear un entorno virtual de Python 3.12 o posterior. Si no tiene instalado Python 3.12 o porsterior por favor siga las instrucciones disponibles en https://docs.python.org/3.12/using/index.html. Si la versión de Python instalada de base es >3.12 ejecuta el siguiente comando:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En caso contrario:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

A continuación instala las dependencias necesarias:

```bash
pip install -r AIVA_2026_maderas/requirements.txt
```

### Python

1. Crea tu fichero python o lanza Python desde el terminal e importa la función `detectar`:

```python
from defect_detector import detectar
```

2. Usa `detectar` para detectar los defectos en una tabla de madera como en el siguiente ejemplo:

```python
result = detectar("imagen.png", "out.xml")
print(result)
```

### C

1. Mueve el código fuente de este repositorio al directorio `include` o similar de tu proyecto:

```bash
mv AIVA_2026_maderas/src/defect_detector.* include/
```

2. Mueve el modelo al directorio `models` de tu proyecto. Si no tienes es directorio crea uno con el siguiente comando `mkdir models`:

```bash
mv AIVA_2026_maderas/models/model.pt models/
```

3. Incluye la función `detectar` desde tú código fuente:

```c
#include "defect_detector.h"
```

4. Compila tú código fuente enlazando las librerías necesarias (Cambia `python3.12` por la versión instalada posterior a 3.12). Por ejemplo:

```bash
gcc src/main.c -I/usr/include/python3.12 -I./include -lpython3.12 -o minimum
```

### Ejemplos de despliegues

Hay disponibles 2 ejemplos distintos de como instalar y usar el detector de maderas. Haga click en la sección correspondiente:

- [Despliegue Mínimo](https://github.com/javizqh/AIVA_2026_maderas/examples/minimum)
- [Despliegue de Desarrollador](https://github.com/javizqh/AIVA_2026_maderas/examples/development)

#### Despliegue en Raspberry Pi

Para este ejemplo se usará el despliegue mínimo como prueba de concepto. Sigue los siguientes pasos:

1. Enciende las Raspberry Pi y conectate por ssh. Si no esta habilitada la conexión por ssh también es posible entrar con la interfaz gráfica, y en caso de que ambas opciones no sean posibles será necesario flashear una nueva imagen en la Raspberry Pi para habilitar ssh (siga la guía oficial en https://www.raspberrypi.com/documentation/computers/getting-started.html#install). En este ejemplo el nombre del host, usuario y contraseña son `alumno`:

```bash
ssh alumno@alumno.local
```

2. Para una instalación sencilla es necesario cambiar el directorio temporal de pip. **IMPORTANTE** Es necesario hacer el export cada vez que se quiera instalar algo de gran tamaño con Pip.

```bash
mkdir  /home/alumno/pip_cache
export TMPDIR=/home/alumno/pip_cache
```

3. Seguimos los pasos del [Despliegue Mínimo](https://github.com/javizqh/AIVA_2026_maderas/examples/minimum) hasta el punto de la ejecución. En el caso de la Raspberry Pi de este ejemplo, la versión de Python instalada de base es la 3.13 por lo que no hace falta la instalación de ninguna versión de Python y habría que reemplazar `python3.12` por `python3.13` a la hora de compilar.

## Tests

Para ejecutar los tests (solo en Python) es necesario seguir los 2 pasos de la sección anterior sobre como ejecutar la aplicación en Python.

Una vez estos pasos se hayan realizado, los tests se lanzan con el siguiente comando:

```bash
python test.py
```

Estos tests comprueban:

- La función se puede llamar correctamente
- La detección de los defectos tiene más de un 80% de precisión
- Solo genera predicciones con más de un 50% de confianza
- Solo genera salidas de los 2 tipos de defectos: nodo y grieta
- El tiempo de inferencia es menor de 1 segundo por imagen
- Si la imagen no existe devuelve un error
- La función se llama correctamente si solo se le pasa la dirección de la imagen
- La función se llama correctamente si se le pasa la dirección de la imagen y la dirección de salida del xml

## Otros

Para entrenar el modelo dirijasé a la [documentación correspondiente](https://github.com/javizqh/AIVA_2026_maderas/blob/main/utils/README.md).
