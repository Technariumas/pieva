from pieva import *
import fastopc as opc
import time

def toRGBBytes(value):
    value = int(value)
    return [(value >> 16) & 0x0000FF, (value >> 8) & 0x0000FF, value & 0x0000FF]

class Screen():
    leds = opc.FastOPC()
    auxscreens = []
    pixelMap = []
    
    def __init__(self, auxscreens = []):
        if None != auxscreens:
            for aux in auxscreens:
                self.auxscreens.append(opc.FastOPC(aux))
        for section in sections:
            self.pixelMap += self.createMapFor(section)
            
    def createMapFor(self, section):
        pixmap = []
        x = section['startX']
        y = section['startY']
        for led in section['pattern']:
            x = x + led['xstep']
            y = y + led['ystep']
            pixmap.append((x, y))
        section['map'] = pixmap
        return pixmap
        
    def getPixelsFor(self, section, bitmap):
        pixels = []
        for i in range(len(section['pattern'])):
            y = section['map'][i][1]
            x = section['map'][i][0]
            pixels += toRGBBytes(bitmap[y, x])
        return pixels


    def send(self, bitmap):
        tosend = []
        startTime = time.time()
        for section in sections:
            tosend += self.getPixelsFor(section, bitmap)
        endTime = time.time()
        print("preparation time: ", (endTime - startTime))
        startTime = time.time()
        self.leds.putPixels(0, tosend)
        endTime = time.time()
        print("pixel push time:  ", (endTime - startTime))
        for aux in self.auxscreens:
            aux.putPixels(0, tosend)
