[![Deploy and test the application in an enviroment similar to production](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/deploy_test.yml/badge.svg?branch=main)](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/deploy_test.yml)
[![Python Linting](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/python_lint.yml/badge.svg?branch=main)](https://github.com/javizqh/AIVA_2026_maderas/actions/workflows/python_lint.yml)

# AIVA_2026_maderas

El proyecto consiste en el desarrollo de un sistema de visión artificial para detectar defectos en tablas de madera. La juguetera artesanal crea piezas de madera a partir de tablas y quiere descartar defectos de dichas tablas para que no estén presentes en las piezas. Con este objetivo se pretende implementar el sistema software en una línea de producción para cribar los defectos. El sistema final será capaz de detectar defectos, localizarlos y proporcionar una medida de la confianza de la detección de los defectos presentes en una tabla de madera. La localización será proporcionada con un bounding box que engloba el defecto, y el factor de confianza con un valor de 0 a 1. Las salidas del sistema serán almacenadas en un archivo XML.

## ¿Cómo usar?

Para poder usar este proyecto tanto en Python como en C (proximamente) es necesario seguir los siguientes pasos para cada uno de ellos, pero primero es necesario clonar el repositorio con el siguiente comando:

```bash
git clone https://github.com/javizqh/AIVA_2026_maderas.git
```

### Python

1. Crea un entorno virtual de Python 3.12. Si no tiene instalado Python 3.12 por favor siga las instrucciones disponibles en https://docs.python.org/3.12/using/index.html.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

3. Crea tu fichero python o lanza Python desde el terminal e importa la función `detect`:

```python
from src.main import detect
```

4. Usa detect para detectar los defectos en una tabla de madera como en el siguiente ejemplo:

```python
result = detect("imagen.png", "out.xml")
print(result)
```

### C

**En progreso**

## Otros

Para entrenar el modelo dirijasé a la [documentación correspondiente](https://github.com/javizqh/AIVA_2026_maderas/blob/main/utils/README.md).
