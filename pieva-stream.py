from pieva import *
from screen import Screen
import numpy as np
import time
import fastopc as opc

bitmap = np.zeros((32, 32)) * 255

from noise import pnoise3, snoise3, pnoise2, snoise2
octaves = 5
freq = 16.0 * octaves


noiseTime = 2000
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

screen = Screen(['127.0.0.1:7891'])

print("eina.. Control+C to stop")
while True:
    for z in range(noiseTime):
        bitmap = noise[:,:,z]
        #print biteleX[0,z], biteleY[0,z]
        startTime = time.time()
        bitmap[int(biteleX[0,z]), int(biteleY[0,z])] = 0x00FF0000 
        #~ bitmap[31,23] = 0x00FFFFFF
        screen.send(bitmap)
        endTime = time.time()
        #print (endTime - startTime)
        timeToWait = targetFrameTime - (endTime - startTime)
        if timeToWait < 0:
            print("late!", timeToWait)
            timeToWait = 0
        time.sleep(timeToWait)
