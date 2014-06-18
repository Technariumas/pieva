import numpy as np


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
        return r.astype(np.int8)
    
    def get32bitColor(self, index):
        return self.palette[index][0] << 16 | self.palette[index][1] << 8 | self.palette[index][2]

