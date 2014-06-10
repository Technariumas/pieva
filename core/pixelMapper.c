#include <Python.h>
#include <stdio.h>
#include <inttypes.h>
#include "noise.h"

#define ALWAYS_INLINE __attribute__((always_inline))

typedef struct {
    const uint8_t *model;
    const uint32_t *bitmap;
    int pixelCount;
} MapArgs_t;

typedef struct {
    const uint8_t width;
    const uint8_t height;
    const uint32_t time;
    const uint8_t octaves;
    const float persistence;
    const float lacunarity;
} GetNoiseArgs_t;

unsigned long frameCounter = 0;

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

inline static void ALWAYS_INLINE map(MapArgs_t args, char *pixels) {
    while (args.pixelCount--) {
        unsigned char x, y, r, g, b;
        
        x = args.model[0];
        y = args.model[1];
        args.model += 2;

        r = (args.bitmap[x + y * 32] >> 16) & 0x000000FF;
        g = (args.bitmap[x + y * 32] >> 8) & 0x000000FF;
        b = args.bitmap[x + y * 32] & 0x000000FF;
        
        pixels[0] = r;
        pixels[1] = g;
        pixels[2] = b;
        pixels += 3;
    }
    frameCounter++;
}



static PyObject* py_get2dNoise(PyObject* self, PyObject* args) {
    GetNoiseArgs_t arguments;
    
    if (!PyArg_ParseTuple(args, "iiliff:map",
        &arguments.width,
        &arguments.height,
        &arguments.time,
        &arguments.octaves,
        &arguments.persistence,
        &arguments.lacunarity)) {
        return NULL;
    }

    //~ PyObject *result = PyBuffer_New(arguments.width * arguments.height);
    //~ if (result) {
        //~ PyObject_AsWriteBuffer(result, (void**) &buffer, &tmp);
        //~ 
        //~ get2dNoise(arguments, buffer);
    //~ }

    return get2dNoise(arguments);
}

static PyObject* py_map(PyObject* self, PyObject* args)
{
    MapArgs_t arguments;
    int modelBytes, bitmapBytes;

    char *pixels;
    PyObject *result = NULL;
    Py_ssize_t tmp;

    if (!PyArg_ParseTuple(args, "t#s#:map",
        &arguments.model, &modelBytes,
        &arguments.bitmap,  &bitmapBytes
        )) {
        return NULL;
    }

    arguments.pixelCount = modelBytes / 2;

    result = PyBuffer_New(arguments.pixelCount * 3);
    if (result) {
        PyObject_AsWriteBuffer(result, (void**) &pixels, &tmp);
        map(arguments, pixels);
    }

    return result;
}

static PyMethodDef native_functions[] = {
    { "map", (PyCFunction)py_map, METH_VARARGS,
        "render(model, bitmap) -- return rendered RGB pixels, as a string\n\n"
        "model -- (x,y) coordinates for each LED, represented as a string of packed 8-bit ints\n"
        "bitmap -- bitmap pixels, 32-bit each, represented as a string of packed 32-bit ints"
    },
    { "get2dNoise", (PyCFunction)py_get2dNoise, METH_VARARGS,
        "get2dNoise -- return a twodimensional array of perlin noise\n\n"
    },
    {NULL}
};

PyDoc_STRVAR(module_doc, "Native-code utilities for faster data structure mangling");

void initpixelMapper(void)
{
    Py_InitModule3("pixelMapper", native_functions, module_doc);
}
