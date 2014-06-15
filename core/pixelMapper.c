#include <Python.h>
#include <inttypes.h>
#include "noise.h"

#define ALWAYS_INLINE __attribute__((always_inline))

typedef struct {
    unsigned int octaves;
    float persistence;
    float lacunarity;
    float wavelength;
    float xScrollSpeed;
    float yScrollSpeed;
    unsigned int amplitude;
    unsigned int offset; 
} Noise_t;

typedef struct {
    const uint8_t *model;
    const uint16_t width;
    const uint16_t height; 
    const float time;
    const uint8_t *palette;
    const uint16_t paletteLength;
    int pixelCount;
    int noiseLayersCount;
    Noise_t *noiseLayers;
} RenderArgs_t;

typedef struct {
    const uint8_t *model;
    const uint32_t *bitmap;
    const uint16_t width;
    const uint16_t height;
    int pixelCount;
} MapArgs_t;

inline static void ALWAYS_INLINE map(MapArgs_t args, char *pixels) {
    while (args.pixelCount--) {
        unsigned char x, y, r, g, b;
        
        x = args.model[0];
        y = args.model[1];
        args.model += 2;

        r = (args.bitmap[x + y * args.height] >> 16) & 0x000000FF;
        g = (args.bitmap[x + y * args.height] >> 8) & 0x000000FF;
        b = args.bitmap[x + y * args.height] & 0x000000FF;
        
        pixels[0] = r;
        pixels[1] = g;
        pixels[2] = b;
        pixels += 3;
    }
}

float getNoise(uint8_t x, uint8_t y, float time, Noise_t noise)
{
	return fbm_noise3((float)x / noise.wavelength + time * noise.xScrollSpeed, (float)y / noise.wavelength + time * noise.yScrollSpeed, time, noise.octaves, noise.persistence, noise.lacunarity) * noise.amplitude + noise.offset;
}

inline static void ALWAYS_INLINE render(RenderArgs_t args, char *pixels) {
    while (args.pixelCount--) {
        uint8_t x = args.model[0];
        uint8_t y = args.model[1];
        args.model += 2;

		int i;
		float noise = 0;
		for(i = 0; i < args.noiseLayersCount; i++) {
			noise += getNoise(x, y, args.time, args.noiseLayers[i]);
		}
		
		int16_t index = (int) noise;
		if(index < 0) {
			index = 0;
		}
		if(index > 255) {
			index = 255;
		}
		
		uint8_t r = args.palette[index * 3];
		uint8_t g = args.palette[index * 3 + 1];
		uint8_t b = args.palette[index * 3 + 2];
        
        pixels[0] = r;
        pixels[1] = g;
        pixels[2] = b;
        pixels += 3;
    }
}

static PyObject* py_map(PyObject* self, PyObject* args)
{
    MapArgs_t arguments;
    int modelBytes, bitmapBytes;

    char *pixels;
    PyObject *result = NULL;
    Py_ssize_t tmp;

    if (!PyArg_ParseTuple(args, "t#s#ii:map",
        &arguments.model, &modelBytes,
        &arguments.bitmap, &bitmapBytes,
        &arguments.width,
        &arguments.height
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

static PyObject* py_render(PyObject* self, PyObject* args)
{
    RenderArgs_t arguments;
    int modelBytes;

    char *pixels;
    PyObject *result = NULL;
    PyObject *noiseLayersList;
    Py_ssize_t tmp;

    if (!PyArg_ParseTuple(args, "IIft#t#O:map",
        &arguments.width,
        &arguments.height,
        &arguments.time,
        &arguments.model, &modelBytes,
        &arguments.palette,
        &arguments.paletteLength,
        &noiseLayersList
        )) {
        return NULL;
    }

    arguments.pixelCount = modelBytes / 2;
    
    if (!PySequence_Check(noiseLayersList)) {
        PyErr_SetString(PyExc_TypeError, "Noise layers list is not a sequence");
        return NULL;
    }    

    arguments.noiseLayersCount = (int) PySequence_Length(noiseLayersList);
    arguments.noiseLayers = PyMem_Malloc(arguments.noiseLayersCount * sizeof arguments.noiseLayers[0]);

	int i;
    for (i = 0; i < arguments.noiseLayersCount; ++i) {
        PyObject *item = PySequence_GetItem(noiseLayersList, i);
        
        if(!PyObject_HasAttrString(item, "octaves")) {
			printf("Noise object %d does not contain octaves\n", i);
			return NULL;
		}

        if(!PyObject_HasAttrString(item, "persistence")) {
			printf("Noise object %d does not contain persistence\n", i);
			return NULL;
		}

        if(!PyObject_HasAttrString(item, "lacunarity")) {
			printf("Noise object %d does not contain lacunarity\n", i);
			return NULL;
		}
        
        Noise_t *n = &arguments.noiseLayers[i];
        
        if (!PyArg_Parse(PyObject_GetAttrString(item, "octaves"), "I:map",
			&n->octaves)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse octaves for noise object %d\n", i);
			return NULL;
		}

        if (!PyArg_Parse(PyObject_GetAttrString(item, "persistence"), "f:map",
			&n->persistence)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse persistence for noise object %d\n", i);
			return NULL;
		}

        if (!PyArg_Parse(PyObject_GetAttrString(item, "lacunarity"), "f:map",
			&n->lacunarity)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse lacunarity for noise object %d\n", i);
			return NULL;
		}


        if (!PyArg_Parse(PyObject_GetAttrString(item, "wavelength"), "f:map",
			&n->wavelength)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse wavelength for noise object %d\n", i);
			return NULL;
		}

        if (!PyArg_Parse(PyObject_GetAttrString(item, "xScrollSpeed"), "f:map",
			&n->xScrollSpeed)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse xScrollSpeed for noise object %d\n", i);
			return NULL;
		}

        if (!PyArg_Parse(PyObject_GetAttrString(item, "yScrollSpeed"), "f:map",
			&n->yScrollSpeed)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse yScrollSpeed for noise object %d\n", i);
			return NULL;
		}

        if (!PyArg_Parse(PyObject_GetAttrString(item, "amplitude"), "I:map",
			&n->amplitude)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse yScrollSpeed for noise object %d\n", i);
			return NULL;
		}

        if (!PyArg_Parse(PyObject_GetAttrString(item, "offset"), "I:map",
			&n->offset)){
            Py_DECREF(item);
            PyMem_Free(arguments.noiseLayers);
			printf("Could not parse offset for noise object %d\n", i);
			return NULL;
		}


        Py_DECREF(item);
    }

    result = PyBuffer_New(arguments.pixelCount * 3);
    if (result) {
        PyObject_AsWriteBuffer(result, (void**) &pixels, &tmp);
        render(arguments, pixels);
    }

    return result;
}

static PyMethodDef native_functions[] = {
    { "render", (PyCFunction)py_render, METH_VARARGS,
        "render(model, bitmap) -- return rendered RGB pixels, as a string\n\n"
        "model -- (x,y) coordinates for each LED, represented as a string of packed 8-bit ints\n"
        "bitmap -- bitmap pixels, 32-bit each, represented as a string of packed 32-bit ints"
    },
    { "map", (PyCFunction)py_map, METH_VARARGS,
        "map(model, bitmap) -- return rendered RGB pixels, as a string\n\n"
        "model -- (x,y) coordinates for each LED, represented as a string of packed 8-bit ints\n"
        "bitmap -- bitmap pixels, 32-bit each, represented as a string of packed 32-bit ints"
    },
    {NULL}
};

PyDoc_STRVAR(module_doc, "Native-code utilities for faster data structure mangling");

void initPixelMapper(void)
{
    Py_InitModule3("PixelMapper", native_functions, module_doc);
}
