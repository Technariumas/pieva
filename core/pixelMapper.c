#include <Python.h>
#include <inttypes.h>

#define ALWAYS_INLINE __attribute__((always_inline))

typedef struct {
    const uint8_t *model;
    const uint32_t *bitmap;
    int pixelCount;
} MapArgs_t;

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
    {NULL}
};

PyDoc_STRVAR(module_doc, "Native-code utilities for faster data structure mangling");

void initPixelMapper(void)
{
    Py_InitModule3("PixelMapper", native_functions, module_doc);
}
