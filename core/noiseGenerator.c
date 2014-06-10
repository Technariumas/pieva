#include <Python.h>
#include <inttypes.h>
#include "noise.h"
#define ALWAYS_INLINE __attribute__((always_inline))

typedef struct {
    const uint8_t width;
    const uint8_t height;
    const float time;
    const uint8_t octaves;
    const float persistence;
    const float lacunarity;
} GetNoiseArgs_t;

inline static PyObject* ALWAYS_INLINE get2dNoise(GetNoiseArgs_t args){
    int i,j;
    PyObject *result = PyList_New(args.width);

    for(i = 0; i < args.width; i++) {
        PyObject *row = PyList_New(args.height);
        for(j = 0; j < args.height; j++) {
            uint8_t noisedot = fbm_noise3((float)i/args.width, (float)j/args.height, args.time, args.octaves, args.persistence, args.lacunarity) * 127 + 128;
            PyList_SetItem(row, j, PyInt_FromLong(noisedot)); 
        }
        PyList_SetItem(result, i, row);
    }
    return result;
}

static PyObject* py_get2dNoise(PyObject* self, PyObject* args) {
    GetNoiseArgs_t arguments;
    
    if (!PyArg_ParseTuple(args, "iififf:map",
        &arguments.width,
        &arguments.height,
        &arguments.time,
        &arguments.octaves,
        &arguments.persistence,
        &arguments.lacunarity)) {
        return NULL;
    }

    return get2dNoise(arguments);
}

static PyMethodDef native_functions[] = {
    { "get2dNoise", (PyCFunction)py_get2dNoise, METH_VARARGS,
        "get2dNoise -- return a twodimensional array of perlin noise\n\n"
    },
    {NULL}
};


PyDoc_STRVAR(module_doc, "Native-code utilities for noise generation");

void initNoiseGenerator(void)
{
    Py_InitModule3("NoiseGenerator", native_functions, module_doc);
}
