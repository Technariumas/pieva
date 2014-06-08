from pieva import *
import fastopc as opc
import time

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
        pixels = []
        for led in pattern:
            x = x + led['xstep']
            y = y + led['ystep']
            pixels += toRGBBytes(bitmap[y, x])
        return pixels


    def send(self, bitmap):
        tosend = []
        startTime = time.time()
        for section in sections:
            tosend += self.getPixelsFor(section['pattern'], section['startX'], section['startY'], bitmap)
        endTime = time.time()
        print("preparation time: ", (endTime - startTime))
        startTime = time.time()
        self.leds.putPixels(0, tosend)
        endTime = time.time()
        print("pixel push time:  ", (endTime - startTime))
        for aux in self.auxscreens:
            aux.putPixels(0, tosend)
