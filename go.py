#!/usr/bin/python
from pieva import *
from screen import Screen
import numpy as np
import time
import fastopc as opc
import random
from core import NoiseGenerator

class NoiseParams:
    octaves = 1
    persistence = 0.5
    lacunarity = 2.0
    wavelength = 32
    xScrollSpeed = 0
    yScrollSpeed = 0
    amplitude = 127
    offset = 128 
    
    def __init__(self, octaves, persistence, lacunarity, wavelength, xScrollSpeed, yScrollSpeed, amplitude, offset):
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.wavelength = wavelength
        self.xScrollSpeed = xScrollSpeed
        self.yScrollSpeed = yScrollSpeed
        self.amplitude = amplitude
        self.offset = offset
        

class ColorPalette:
    palette = [
    ]

    def __init__(self, startColor = None, endColor = None, CSVfilename=None):
        if startColor != None and endColor != None:
            self.palette = self.generatePalette(startColor, endColor)
        elif CSVfilename != None:
            self.palette = self.readCSVPalette(CSVfilename)    

        self.packed = np.array(self.palette).astype(np.int8).tostring()

    def generatePalette(self, startColor, endColor):
       r = np.linspace(startColor[0], endColor[0], 256) 
       g = np.linspace(startColor[1], endColor[1], 256) 
       b = np.linspace(startColor[2], endColor[2], 256)
       print np.array([r,g,b]).T
       return np.array([r,g,b]).T

    def readCSVPalette(self, SNSfilename):
        r = np.genfromtxt(SNSfilename, delimiter=',')
        return r
        
        

CSVfilename="palettes/rainbow"

width = 140
height = 140

sun = NoiseParams(
    octaves = 1, 
    persistence = 0.5, 
    lacunarity = 2.0, 
    wavelength = width * 8.0, 
    xScrollSpeed = 1, 
    yScrollSpeed = 0, 
    amplitude = 95, 
    offset = 1)

grass = NoiseParams(
    octaves = 5, 
    persistence = 0.702, 
    lacunarity = 2.0, 
    wavelength = width / 8, 
    xScrollSpeed = 0, 
    yScrollSpeed = 5, 
    amplitude = 80, 
    offset = 80)

mainPalette = ColorPalette(CSVfilename=CSVfilename)

screen = Screen(sections)#, ['127.0.0.1:7891'])

targetFPS = 24
targetFrameTime = 1./targetFPS
timeCounter = int(random.random() * 65535)
print("eina.. Control+C to stop")
while True:
    startTime = time.time()
    screen.render(width, height, timeCounter/640., [grass, sun], mainPalette)
    endTime = time.time()
    timeToWait = targetFrameTime - (endTime - startTime)
#    print"Frame time: ", (endTime - startTime)
    if timeToWait < 0:
        print("late!", timeToWait)
        timeToWait = 0
    time.sleep(timeToWait)
    timeCounter +=1
