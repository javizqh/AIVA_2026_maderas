#ifndef INCLUDE_FREQUENCY_HPP_
#define INCLUDE_FREQUENCY_HPP_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

/**
* Función que detecta fallos en la tabla.
*
* input parameters
* =======================
* image_filename: nombre del fichero que contiene la imagen.
* xml_file: nombre del fichero XML donde se escribe el resultado. Si NULL no hay que escribir nada
*
* return:
* Un puntero a un array de enteros. El primero entero corresponde al número de rectangulos detectados.
* 0 implica que no se ha detectado ninguno.
* Cada rectángulo se compone de 5 enteros correspondientes a x0,y0,width, height y conf.
*/
int* detectar(char *image_filename, char *xml_file){
    Py_Initialize();
    PyObject *pArgs;
    PyObject *pResult = NULL;
    PyObject *pName, *pModule, *pFunc, *pImage, *pXML;

    PyRun_SimpleString("import sys; sys.path.append('./include')");

    pName = PyUnicode_FromString("defect_detector");
    pModule = PyImport_Import(pName);

    pFunc = PyObject_GetAttrString(pModule,"detectar");

    if (xml_file == NULL) {
    }

    // 1. Create Python objects for the arguments
    pImage = PyUnicode_FromString(image_filename);
    if (xml_file != NULL) {
        pXML = PyUnicode_FromString(xml_file);
        if (!pXML) {
            // Handle error: Failed to create one of the objects
            Py_XDECREF(pImage);
            Py_XDECREF(pXML);
            return NULL; 
        }
    }

    if (!pImage) {
        // Handle error: Failed to create one of the objects
        Py_XDECREF(pImage);
        return NULL; 
    }

    // 2. Create a tuple to hold the positional arguments (3 arguments)
    if (xml_file == NULL) {
        pArgs = PyTuple_New(1);
    } else {
        pArgs = PyTuple_New(2);
    }

    if (!pArgs) {
        Py_XDECREF(pImage); // XDECREF handles NULL gracefully
        // Py_XDECREF(pXML);
        return NULL;
    }

    // 3. Set the tuple items (Steals the references to the arguments!)
    // NOTE: PyTuple_SetItem 'steals' the reference, so we don't DECREF them afterward
    PyTuple_SetItem(pArgs, 0, pImage);
    if (xml_file != NULL) {
        PyTuple_SetItem(pArgs, 1, pXML);
    }

    // 4. Call the function (pFunc) with the arguments (pArgs)
    // NOTE: For simple positional arguments, we use PyObject_CallObject
    pResult = PyObject_CallObject(pFunc, pArgs);

    // 5. Cleanup the argument tuple
    Py_DECREF(pArgs); // We own the reference to the tuple

    if (pResult == NULL) {
        PyErr_Print();
        fprintf(stderr, "Error calling Python function with PyObject_CallObject!\n");
        return NULL;
    }
    
    Py_ssize_t list_size = PyList_Size(pResult);

    int* result = malloc(list_size * sizeof(int));

    for (Py_ssize_t j = 0; j < list_size; j++) {
        result[j] = (int) PyFloat_AsDouble(PyList_GetItem(pResult, j));
    }

    Py_DECREF(pResult);
    
    Py_Finalize();

    return result;
};

#endif
