#create colour palettes with sns
#reguires seaborn (http://www.stanford.edu/~mwaskom/software/seaborn)

from __future__ import division
import numpy as np
import seaborn as sns
import matplotlib as mpl


def make_palette_array(pal):
    cm = mpl.colors.ListedColormap(list(pal))
    r = cm((np.arange(256)))
    r = 255.999*r[:, 0:3]
    return r.astype(np.uint8)	

def get_palette():
	pal = sns.color_palette("RdPu_r", 256)
	return make_palette_array(pal)
