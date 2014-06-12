import numpy as np

class ColorPalette:
    palette = [
    ]

    def __init__(self, startColor = None, endColor = None):
        if startColor != None and endColor != None:
            self.palette = self.generatePalette(startColor, endColor)
        print self.palette
        self.packed = np.array(self.palette).astype(np.int8).tostring()

    def generatePalette(self, startColor, endColor):
       r = np.linspace(startColor[0], endColor[0], 256) 
       g = np.linspace(startColor[1], endColor[1], 256) 
       b = np.linspace(startColor[2], endColor[2], 256)
       return np.array([r,g,b]).T
        

startColor = [0, 128, 40]
endColor = [255, 255, 0]
mainPalette = ColorPalette(startColor, endColor)

import scipy.misc.pilutil as smp
bitmap=np.zeros([256, 256, 3])
for i in range(256):
    bitmap[:,i,:]= mainPalette.palette[i]
img = smp.toimage(bitmap )       
img.show() 
