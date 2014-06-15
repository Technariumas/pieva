#create colour palettes with sns
#reguires seaborn (http://www.stanford.edu/~mwaskom/software/seaborn)

from __future__ import division
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.image as mpimg
import sys



def make_SNS_palette(paletteFilename):
		#flat = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
		#pal = sns.color_palette(flat, 256)
		pal = sns.color_palette("husl", 256)
		cm = mpl.colors.ListedColormap(list(pal))
		r = cm((np.arange(256)))
		r = 255.999*r[:, 0:3]
		np.savetxt(paletteFilename, r, delimiter=",")

def makeBitmapPalette(paletteFilename):
		#Warning -- TIFF images supported only. If using 16-bit BMPs, which may work, adjust the np.savetxt() call
		img=mpimg.imread(paletteFilename)[0]
		np.savetxt(paletteFilename[0:-5], img, delimiter=",")



paletteFilename = sys.argv[1]
makeBitmapPalette("palettes/"+paletteFilename)


