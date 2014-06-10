import numpy as np
import fastopc
class PixelController(object):
    
    
    def __init__(self, leds):
        self.leds = np.array(leds)
        packModel()
        
    def packModel(self):
        self.ledsPacked = self.leds.astype(np.int8).tostring()
    
    def drawFrame(self, bitmap):
        # Calculate our main cloud effect (Native code)

        # Pack together our raw cloud pixels and NumPy DMX array, send it all off over OPC.
        self.opc.putPixels(0, cloudPixels)
