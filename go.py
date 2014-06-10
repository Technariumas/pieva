#!/usr/bin/python
from pieva import *
from screen import Screen
import numpy as np
import time
import fastopc as opc
from core import NoiseGenerator

class NoiseParams:
    octaves = 1
    persistence = 0.5
    lacunarity = 2.0
    def __init__(self, octaves, persistence, lacunarity):
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        
mainNoiseParams = NoiseParams(5, 0.7, 2.0)

targetFPS = 24
targetFrameTime = 1./targetFPS
screen = Screen(sections, ['127.0.0.1:7891'])

timeCounter = 0
print("eina.. Control+C to stop")
while True:
    bitmap = NoiseGenerator.get2dNoise(32,32, timeCounter/20.0, mainNoiseParams.octaves, mainNoiseParams.persistence, mainNoiseParams.lacunarity)
    biteleXX = NoiseGenerator.get2dNoise(1,10, timeCounter/20., 7, 0.5, 2)
    biteleYY = NoiseGenerator.get2dNoise(1,10, 2+timeCounter/20., 7, 0.5, 2)
    #print biteleXY
    startTime = time.time()

    bitmap[int(biteleXX[0][9] / 255. * 15 + 16) - 7][int(biteleYY[0][9] / 255. * 15 + 16) -7] = 0x00FFFF00 
    screen.send(bitmap)

    endTime = time.time()
    timeToWait = targetFrameTime - (endTime - startTime)
    print("Frame time: ", (endTime - startTime))
    if timeToWait < 0:
        print("late!", timeToWait)
        timeToWait = 0
    time.sleep(timeToWait)
    timeCounter +=1
