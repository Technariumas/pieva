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

    startTime = time.time()

    #bitmap[int(biteleX[0,z])][int(biteleY[0,z])] = 0x00FF0000 
    screen.send(bitmap)

    endTime = time.time()
    timeToWait = targetFrameTime - (endTime - startTime)
    print("Frame time: ", (endTime - startTime))
    if timeToWait < 0:
        print("late!", timeToWait)
        timeToWait = 0
    time.sleep(timeToWait)
    timeCounter +=1
