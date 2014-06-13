#include <Python.h>
#include <inttypes.h>
#include "noise.h"

#define ALWAYS_INLINE __attribute__((always_inline))

typedef struct {
    const uint8_t *model;
    const uint16_t width;
    const uint16_t height; 
    const float time;
    const uint8_t octaves;
    const float persistence;
    const float lacunarity;
    const uint8_t *palette;
    const uint16_t paletteLength;
    int pixelCount;
} MapArgs_t;



float getNoise(uint8_t x, uint8_t y, float time, float wavelength, float xScrollSpeed, float yScrollSpeed, uint8_t octaves, float persistence, float lacunarity)
{
	return fbm_noise3((float)x / wavelength + xScrollSpeed, (float)y / wavelength + yScrollSpeed, time, octaves, persistence, lacunarity);
}

inline static void ALWAYS_INLINE render(MapArgs_t args, char *pixels) {
    while (args.pixelCount--) {
        uint8_t x = args.model[0];
        uint8_t y = args.model[1];
        args.model += 2;

		//float v = fbm_noise3((float)x /args.width/8.0 + args.time, (float)y/args.height/8.0, args.time, 1, 0.5, 2.0);
		float sun = getNoise(x, y, args.time, args.width * 8.0, args.time, 0, 1, 0.5, 2.0);
		//float bg = fbm_noise3((float)x / args.width * 8.5, (float)y/args.height * 8.5 + args.time *5, args.time, 5, 0.702, 2.0);
		float grass = getNoise(x, y, args.time, args.width / 8, 0, args.time * 5, 5, 0.702, 2.0);
		
		uint8_t grassAmplitude = 80;
		uint8_t grassOffset = 80;

		uint8_t sunAmplitude = 95;
		uint8_t sunOffset = 0;
		
		float noise = 0.0;
		noise += (grass * grassAmplitude + grassOffset);
		noise += (sun * sunAmplitude + sunOffset);
		
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
    int modelBytes;

    char *pixels;
    PyObject *result = NULL;
    Py_ssize_t tmp;

    if (!PyArg_ParseTuple(args, "iift#t#iff:map",
        &arguments.width,
        &arguments.height,
        &arguments.time,
        &arguments.model, &modelBytes,
        &arguments.palette,
        &arguments.paletteLength,
        &arguments.octaves,
        &arguments.persistence,
        &arguments.lacunarity
        )) {
        return NULL;
    }

    arguments.pixelCount = modelBytes / 2;

    result = PyBuffer_New(arguments.pixelCount * 3);
    if (result) {
        PyObject_AsWriteBuffer(result, (void**) &pixels, &tmp);
        render(arguments, pixels);
    }

    return result;
}

static PyMethodDef native_functions[] = {
    { "map", (PyCFunction)py_map, METH_VARARGS,
        "render(model, bitmap) -- return rendered RGB pixels, as a string\n\n"
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
