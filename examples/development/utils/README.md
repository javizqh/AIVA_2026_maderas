# Instrucciones para entrenar el modelo

Para entrenar el modelo hay que seguir los siguientes pasos

## 1. Instalar dependencias extra

Ejecuta el siguiente comando:

```bash
source .venv/bin/activate
pip install -r utils_requirements.txt
```

## 2. Generar las etiquetas en formato YOLO

Para este paso es necesario seleccionar los tipos de cada defecto. Ejecuta los siguientes comandos:

```bash
cd utils
python train.py --create
cd ..
```

## 3. Mover las etiquetas a un nuevo directorio

En este paso moveremos las etiquetas generadas anteriormente a un nuevo directorio. Ejecuta los siguientes comandos:

```bash
mkdir dataset_yolo
cd dataset_yolo
mkdir images labels
cd images
mkdir train val test
cd ../labels
mkdir train val test
cd ..
cp dataset/*.png dataset_yolo/images
mv dataset/*.txt dataset_yolo/labels
```

## 4. Dividir el dataset en Entrenamiento, Validación y Test

La división será estratificada y en 70%, 15% y 15% respectivamente. Ejecuta los siguientes comandos:

```bash
cd utils
python train.py --split
cd ..
```

## 5. Crear el fichero de configuración

Crea el fichero **data.yaml** dentro del directorio **dataset_yolo** con el siguiente contenido:

```yaml
names:
  0: nudo
  1: grieta
path: ./dataset_yolo
test: images/test
train: images/train
val: images/val
```

## 6. Entrenar el modelo

Ejecuta el siguiente comando para entrenar el modelo:

```bash
python train.py --train
```
