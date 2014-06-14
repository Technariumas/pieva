#!/usr/bin/python
from pieva import *
from screen import Screen
import numpy as np
import time
import fastopc as opc
from core import NoiseGenerator
from create_palette import *


class NoiseParams:
    width = 120
    height = 120
    octaves = 1
    persistence = 0.5
    lacunarity = 2.0
    def __init__(self, width, height, octaves, persistence, lacunarity):
        self.width = width
        self.height = height
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        
mainNoiseParams = NoiseParams(140, 140, 5, 0.7, 2.0)

class ColorPalette:
    palette = [
    ]

    def __init__(self, startColor = None, endColor = None):
        if startColor != None and endColor != None:
            self.palette = self.generatePalette(startColor, endColor)
        self.packed = np.array(self.palette).astype(np.int8).tostring()

    def generatePalette(self, startColor, endColor):
       r = np.linspace(startColor[0], endColor[0], 256) 
       g = np.linspace(startColor[1], endColor[1], 256) 
       b = np.linspace(startColor[2], endColor[2], 256)
       print np.array([r,g,b]).T
       return np.array([r,g,b]).T
        

startColor = [0, 128, 20]
endColor = [255, 255, 0]
mainPalette = ColorPalette(startColor, endColor)

screen = Screen(sections)#, ['127.0.0.1:7891'])

targetFPS = 24
targetFrameTime = 1./targetFPS
timeCounter = 0
print("eina.. Control+C to stop")
while True:
    bitmap = NoiseGenerator.get2dNoise(mainNoiseParams.width, mainNoiseParams.height, timeCounter/20.0, mainNoiseParams.octaves, mainNoiseParams.persistence, mainNoiseParams.lacunarity, mainPalette.packed)
#    biteleXX = NoiseGenerator.get2dNoise(1, 10, timeCounter/20., 7, 0.5, 2)
#    biteleYY = NoiseGenerator.get2dNoise(1, 10, 2+timeCounter/20., 7, 0.5, 2)
    #print biteleXY
    startTime = time.time()

#    bitmap[int(biteleXX[0][9] / 255. * 15 + 16) - 7][int(biteleYY[0][9] / 255. * 15 + 16) -7] = 0x00FFFF00 
    screen.send(bitmap)

    endTime = time.time()
    timeToWait = targetFrameTime - (endTime - startTime)
    print"Frame time: ", (endTime - startTime), "\r",
    if timeToWait < 0:
        print("late!", timeToWait)
        timeToWait = 0
    time.sleep(timeToWait)
    timeCounter +=1
