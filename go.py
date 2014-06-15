#!/usr/bin/python
from pieva import *
from palette import ColorPalette
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
        
paletteFileCSV="palettes/green_grass"

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
    offset = 140)

grass = NoiseParams(
    octaves = 4, 
    persistence = 0.702, 
    lacunarity = 2.0, 
    wavelength = width / 8, 
    xScrollSpeed = 0, 
    yScrollSpeed = 5, 
    amplitude = 120, 
    offset = 120)

mainPalette = ColorPalette(CSVfilename=paletteFileCSV)

screen = Screen(sections)#, ['127.0.0.1:7891'])

from bottle import route, run, template
from threading import Thread

@route('/color/<r>/<g>/<b>')
def index(r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    print " !!!!!!!!!!! ", r, g, b
    mainPalette.regenerate([r,g,b], [g,r,b]);
    return template('ok')

def runBottle():
    run(host="ieva.local", port='80')
server = Thread(target = runBottle)
server.setDaemon(True)
server.start()

time.sleep(1)

targetFPS = 24
targetFrameTime = 1./targetFPS
timeCounter = 0#int(random.random() * 65535)
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
