from pieva import *
import fastopc as opc
import numpy as np

def toRGBBytes(value):
    value = int(value)
    return [(value >> 16) & 0x0000FF, (value >> 8) & 0x0000FF, value & 0x0000FF]

class Screen():
    leds = opc.FastOPC()
    auxscreens = []

    def __init__(self, auxscreens = []):
        if None != auxscreens:
            for aux in auxscreens:
                self.auxscreens.append(opc.FastOPC(aux))
        
    def getPixelsFor(self, pattern, x, y, bitmap):
        pixels = np.empty([0])
        for led in pattern:
            x = x + led['xstep']
            y = y + led['ystep']
            pixels = np.append(pixels, [toRGBBytes(bitmap[y, x])])
        return pixels


    def send(self, bitmap):
        tosend = np.empty([0])
        for section in sections:
            tosend = np.append(tosend, self.getPixelsFor(section['pattern'], section['startX'], section['startY'], bitmap))
        self.leds.putPixels(0, tosend)
        for aux in self.auxscreens:
            aux.putPixels(0, tosend)
