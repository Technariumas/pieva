from pieva import *
import fastopc as opc
import numpy as np
import time

import sys 

del sys.path[0]
sys.path.append('')

import core.pixelMapper

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
        self.pixelMapPacked = np.array(self.pixelMap).astype(np.int8).tostring()
            
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
        pixels = [None] * len(section['pattern'])
        for i in range(len(section['pattern'])):
            y = section['map'][i][1]
            x = section['map'][i][0]
            pixels[i] = toRGBBytes(bitmap[y, x])
        return pixels

    def send(self, bitmap):
        bitmapPacked = bitmap.astype(np.int32).tostring()
        tosend = core.pixelMapper.map(self.pixelMapPacked, bitmapPacked)
        self.leds.putPixels(0, tosend)

    def sendold(self, bitmap):
        tosend = [None] * 3072
        
        startTime = time.time()
        ledsSent = 0
        for section in sections:
            for i in range(len(section['pattern'])):
                y = section['map'][i][1]
                x = section['map'][i][0]
                value = int(bitmap[y, x])
                #toRGBBytes(bitmap[y, x])
                tosend[ledsSent] =  ((value >> 16) & 0x0000FF)
                ledsSent += 1
                tosend[ledsSent] =  ((value >> 8) & 0x0000FF)
                ledsSent += 1
                tosend[ledsSent] =  (value & 0x0000FF)
                ledsSent += 1
            
        #tosend += self.getPixelsFor(section, bitmap)
        endTime = time.time()
        print("preparation time: ", (endTime - startTime))
        
        startTime = time.time()
        self.leds.putPixels(0, tosend)
        endTime = time.time()
        print("pixel push time:  ", (endTime - startTime))
        
        for aux in self.auxscreens:
            aux.putPixels(0, tosend)
