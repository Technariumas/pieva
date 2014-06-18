from pieva import *
import fastopc as opc
import numpy as np
import time
import struct
import sys 

del sys.path[0]
sys.path.append('')

import core.PixelMapper

def toRGBBytes(value):
    value = int(value)
    return [(value >> 16) & 0x0000FF, (value >> 8) & 0x0000FF, value & 0x0000FF]

class Screen():
    opcServers = []
    pixelMap = []
    dimmBy = 0
    
    def __init__(self, ledStrandModel, auxscreens = []):
        for section in ledStrandModel:
            self.pixelMap += self.createMapFor(section)
        self.pixelMapPacked = np.array(self.pixelMap).astype(np.int8).tostring()
        
        print min(np.array(self.pixelMap).T[0]), " - ", max(np.array(self.pixelMap).T[0])
        print min(np.array(self.pixelMap).T[1]), " - ", max(np.array(self.pixelMap).T[1])
        self.opcServers.append(opc.FastOPC())
        if None != auxscreens:
            for aux in auxscreens:
                self.opcServers.append(opc.FastOPC(aux))
            
    def createMapFor(self, section):
        pixmap = []
        x = section['startX']
        y = section['startY']
        if x < 0 or y < 0:
            print "Map pointing to negative pixels!"
            exit(1)
        for led in section['pattern']:
            x = x + led['xstep']
            y = y + led['ystep']
            pixmap.append((x, y))
        return pixmap
    
    def dimm(self, dimm):
        self.dimmBy = dimm
    
    def send(self, bitmap):
        bitmapPacked = bitmap.astype(np.uint32).tostring()#struct.pack('I'*len(bitmap)*len(bitmap[0]), *(j for i in bitmap for j in i)) 
        tosend = core.PixelMapper.map(self.pixelMapPacked, bitmapPacked, len(bitmap[0]), len(bitmap), self.dimmBy)
        for out in self.opcServers:
            out.putPixels(0, tosend)

    def render(self, width, height, time, noiseList, palette):
        tosend = core.PixelMapper.render(width, height, time, self.pixelMapPacked, palette.packed, noiseList, self.dimmBy)
        for out in self.opcServers:
            out.putPixels(0, tosend)
