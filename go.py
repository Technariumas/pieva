#!/usr/bin/python
from pieva import *
from screen import Screen
import numpy as np
import time
import fastopc as opc
from core import pixelMapper

bitmap = np.zeros((32, 32)) * 255

from noise import pnoise3, snoise3, pnoise2, snoise2
octaves = 5
freq = 16.0 * octaves


noiseTime = 2
noise = np.zeros([32,32,noiseTime])
biteleX = np.zeros([32,noiseTime])
biteleY = np.zeros([32,noiseTime])

def generateNoise(width, height, noiseTime = 2000):
    print('generating noise')
    for z in range(noiseTime):
        for x in range(width):
            for y in range(height):
                v = snoise3(x / freq, y / freq, z / freq, octaves, persistence=0.7)
                noise[x,y,z] = (int(v * 20.0 + 20) << 16) | (int(v * 127.0 + 128) << 8) | (int(40 * v) + 80)
#                print '\r', z, ' of ', noiseTime,
            biteleX[x,z] = int(snoise2(x / 16., z / 16., 4, base=0, repeaty = noiseTime) * 15.0 + 16)
            biteleY[x,z] = int(snoise2(x / 16., z / 16., 4, base=1, repeaty = noiseTime) * 15.0 + 16)
    print ("\nDone")

generateNoise(32, 32, noiseTime)
targetFPS = 24
targetFrameTime = 1./targetFPS

screen = Screen()#['127.0.0.1:7891'])

frameCount = 0
print("eina.. Control+C to stop")
while True:
    for z in range(noiseTime):
        bitmap = list(pixelMapper.get2dNoise(32,32, frameCount, 5,0.7,2))

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
        frameCount +=1
