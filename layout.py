import numpy as np
from pieva import *
from argparse import ArgumentParser

DEFAULT_SPACING = 0.125  # m
spacing = DEFAULT_SPACING
origin = {'x':-2 + 0.125/2, 'y':-2 + 0.125/2}

def toOPCLayout(pattern, startFrom):
    x = origin['x'] + startFrom['x'] * spacing
    y = origin['x'] + startFrom['y'] * spacing
    lines = []
    for led in pattern:
        x = x + led['xstep'] * spacing
        y = y + led['ystep'] * spacing
        z = 0
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' % (x, y, z))
    return ',\n'.join(lines)

def outputLayout():
    lines = []
    for section in sections:
        lines.append(toOPCLayout(section['pattern'], {'x':section['startX'],'y':section['startY']}))
    print '[\n' + '\n,'.join(lines) + '\n]'

def toFadecandyMapping(pattern, previousLength):
    return "[0, %d, %d, %d]" % (0,previousLength,len(pattern))

def splitToFadecandies(sections):
    fcSections = [[]]
    fcIndex = 0
    fcPixelCount = 0
    for section in sections:
        if fcPixelCount + len(section['pattern']) < 512:
            fcSections[fcIndex].append(section)
        else:
            fcSections.append([])
            fcIndex = fcIndex + 1
            fcPixelCount = 0
            fcSections[fcIndex].append(section)
        fcPixelCount = fcPixelCount + len(section['pattern'])
    return fcSections
            
def outputMap():
    totalPixels = 0
    fcSections = splitToFadecandies(sections)
    for fadecandy in fcSections:
        fcPixels = 0
        lines = []
        for section in fadecandy:
            firstOPCPixel = totalPixels
            firstOutputPixel = fcPixels
            sectionPixelCount = len(section['pattern'])
            lines.append("\t\t\t\t[0, %d, %d, %d, \"%s\"]" % (firstOPCPixel, firstOutputPixel, sectionPixelCount, rgbRemap))
            totalPixels = totalPixels + sectionPixelCount
            fcPixels = fcPixels + 64
        print "\t\t\t\"map\": [\n" + ",\n".join(lines) + "\n\t\t\t]\n"

    

parser = ArgumentParser(description = "Process the layout and output different representations")
group = parser.add_mutually_exclusive_group()
group.add_argument("--layout", action="store_true", default=True, help="generates OPC pixel layout for gl_server")
group.add_argument("--map", action="store_true", default=False)
parser.add_argument("--layout_spacing", action="store", default=DEFAULT_SPACING, help="specifies pixel spacing for OPC layout in meters")
parser.add_argument("--rgb", action="store", default="rgb", help="specifies pixel spacing for OPC layout in meters")
cliargs = parser.parse_args()

spacing = cliargs.layout_spacing
rgbRemap = cliargs.rgb
if cliargs.map:
    outputMap()
elif cliargs.layout:
    outputLayout()
