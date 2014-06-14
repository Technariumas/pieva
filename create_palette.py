#create colour palettes with sns
#reguires seaborn (http://www.stanford.edu/~mwaskom/software/seaborn)

from __future__ import division
import numpy as np
import seaborn as sns
import matplotlib as mpl

def get_palette(paletteFilename):
		pal = sns.color_palette("RdPu_r", 258)
		#pal = sns.blend_palette(paletteParams, 256)
		cm = mpl.colors.ListedColormap(list(pal))
		r = cm((np.arange(256)))
		r = 255.999*r[:, 0:3]
		np.savetxt(paletteFilename, r, delimiter=",")

get_palette("palettes/pink")
