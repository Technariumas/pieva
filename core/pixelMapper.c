#include <Python.h>
#include <stdio.h>

#define ALWAYS_INLINE __attribute__((always_inline))

typedef struct {
    const unsigned char *model;
    const unsigned char *bitmap;
    int pixelCount;
} MapArgs_t;

inline static void ALWAYS_INLINE map(MapArgs_t args, char *pixels) {
    while (args.pixelCount--) {
        unsigned char x, y, r, g, b;
        
        x = args.model[0];
        y = args.model[1];
        args.model += 2;
        
        r = args.bitmap[0];
        g = args.bitmap[1];
        b = args.bitmap[2];
        args.bitmap += 3;
        
        pixels[0] = r;
        pixels[1] = g;
        pixels[2] = b;
        pixels += 3;
    }
}


static PyObject* py_map(PyObject* self, PyObject* args)
{
    MapArgs_t arguments;
    int i, modelBytes, bitmapBytes;

    char *pixels;
    PyObject *result = NULL;
    Py_ssize_t tmp;

    if (!PyArg_ParseTuple(args, "t#t#:map",
        &arguments.model, &modelBytes,
        &arguments.bitmap,  &bitmapBytes)) {
        return NULL;
    }
    //~ printf("got %d bytes in model and %d bytes in bitmap\n", modelBytes, bitmapBytes);

    arguments.pixelCount = modelBytes / 2;

    result = PyBuffer_New(arguments.pixelCount * 3);
    if (result) {
        PyObject_AsWriteBuffer(result, (void**) &pixels, &tmp);
        map(arguments, pixels);
    }

    //PyMem_Free(ca.lightning);
    return result;
}

static PyMethodDef cloud_functions[] = {
    { "map", (PyCFunction)py_map, METH_VARARGS,
        "render(model, matrix, colors, contrast, lightning) -- return rendered RGB pixels, as a string\n\n"
        "model -- (x,y,z) coordinates for each LED, represented as a string of packed 32-bit floats\n"
        "matrix -- List of 16 floats; a column-major 4x4 matrix which model coordinates are multiplied by\n"
        "colors -- (r,g,b) base color for each pixel, as a string of packed 32-bit floats\n"
        "contrast -- Proportion of base color to modulate with noise field\n"
        "lightning -- List of lightning points, in model space. Each one is an (x, y, z, r, g, b, falloff) tuple\n"
    },
    {NULL}
};

PyDoc_STRVAR(module_doc, "Native-code cloud lighting effect core");

void initpixelMapper(void)
{
    Py_InitModule3("pixelMapper", cloud_functions, module_doc);
}
