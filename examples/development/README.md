# Despliegue mínimo

Este despliegue sirve de ejemplo de como una aplicación puede usar la función para la detección de defectos en la madera al igual que para seguir desarrollando la detección.

## Instalación

Estos pasos son para ejecutar el ejemplo que se provee dentro del repositorio. Para crear tú propio ejemplo siga los pasos de la documentación principal.

1. Clonar el repositorio

```bash
git clone https://github.com/javizqh/AIVA_2026_maderas.git
cd AIVA_2026_maderas
```

2. Dirigase al directorio de este ejemplo:

```bash
cd examples/development
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

4. Instalar las dependencias de Python.

```bash
pip install -r utils_requirements.txt
```

5. Compila tú código fuente enlazando las librerías necesarias:

```bash
gcc src/main.c -I/usr/include/python3.12 -lpython3.12 -o development
```

6. Ejecuta el ejemplo

```bash
./development
```

## Tests

Para ejecutar los tests (solo en Python) se ejecuta el siguiente comando:

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

## Entrenamiento del modelo

Para entrenar el modelo dirijasé a la [documentación correspondiente](https://github.com/javizqh/AIVA_2026_maderas/blob/main/utils/README.md).
