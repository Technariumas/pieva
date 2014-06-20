import svg.path
import numpy as np

section1path = svg.path.parse_path("m 2546.1,2625.5499 -233.7,-233.7 233.7,-233.7 77.9,-233.7 0,-311.6 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,77.9 -77.9,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 77.9,-233.7 0,-311.6 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,77.9 -233.7,-77.9 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 -77.9,-233.7 -233.7,77.9 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 0,-311.6 77.9,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 -77.9,-233.7 -233.7,77.9 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 0,-311.6 77.9,-233.7 233.7,-233.7 -233.7,-233.7")
centersectionpath = svg.path.parse_path("m 2546.1,2625.5499 -233.7,-233.7 233.7,-233.7 77.9,-233.7 0,-311.6 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,77.9 -77.9,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 77.9,-233.7 0,-311.6 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,77.9 -233.7,-77.9 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 -77.9,-233.7 -233.7,77.9 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7 0,-311.6 77.9,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 233.7,-233.7 -77.9,-233.7 -233.7,77.9 -233.7,233.7 -233.7,233.7 -233.7,233.7 -233.7,233.7")
cornerpath = svg.path.parse_path("m 2547.8818,2628.9576 -241.7259,-240.2246 243.2273,-229.7147 76.5716,-235.7204 -1.5014,-312.2919 -231.2161,232.7176 -235.7204,232.7175 -232.7175,237.2218 -237.2218,235.7203 -232.7176,76.5716 -75.0701,-234.2189 235.7203,-235.7204 231.2162,-225.2105 237.2217,-241.726 229.7148,-234.219 232.7175,-229.7147 84.0786,-232.71756 -4.5042,-316.79615 -229.7147,231.21615 -235.7204,238.72316 -234.2189,232.7176 -240.2246,234.2189 -234.219,235.7204 -229.7147,237.2217 -235.72037,228.2134 -234.21895,232.7175 -235.72036,81.0758 -234.21895,-79.5744 237.22176,-237.2217 241.72597,-232.7176 219.20492,-229.7147 244.72878,-235.7204 232.7175,-231.2161 231.2162,-241.726 235.7204,-231.21616 234.2189,-237.22176 235.7204,-231.21614 -85.58,-229.71475 -229.7148,79.57439 -229.7147,226.71194 -234.219,237.22176 -234.2189,234.21895 -235.7204,241.72597 -232.71754,228.2133 -240.22457,231.2162 -240.22457,4.5042 93.08702,-235.7204 229.71475,-237.2217 231.21614,-235.72037 241.72597,-231.21615 228.2133,-228.21334 6.0057,-7.50702")
centerpath = svg.path.parse_path("m -881.5,2625.5499 77.9,-77.9 -77.9,-77.9 0,-155.8 0,-233.7 77.9,155.8 0,155.8 77.9,-155.8 0,-77.9 77.9,-77.9 77.9,77.9 77.9,-77.9 77.9,155.8 77.9,77.9 77.9,155.8 -155.8,-77.9 -155.8,-77.9 0,155.8 77.9,77.9 -155.8,0")

section1 = []
corner=[]
centersection = []
center = []

def toSection(path):
    startx = np.real(path[0].start)
    starty = np.imag(path[0].start)
    section=[]
    lastpoint = None
    for subpath in path:
        if lastpoint == None:
            section.append(dict(xstep=0, ystep=0))
            lastpoint = subpath.start

        dx = np.round((np.real(subpath.end) - np.real(lastpoint))/77.9323)
        dy = np.round((np.imag(subpath.end) - np.imag(lastpoint))/77.9323)
        section.append(dict(xstep=dx, ystep=dy))
        lastpoint = subpath.end
    return section
#points copy pasted from SVG file, could not be bothered to do a proper svg import for now.


#points = np.array(svgpoints)
#points = np.round(points / 77.9323).astype(np.int8)
#section1 = [dict(xstep=x, ystep=y) for x,y in points]
#print segment1, len(segment1)

section1 = toSection(section1path)
corner = toSection(cornerpath)
centersection = toSection(centersectionpath)
center = toSection(centerpath)

def turnMinus90(pattern):
    turned = []
    for point in pattern:
        newpoint = dict(xstep = -point['ystep'], 
                        ystep = point['xstep'])
        turned.append(newpoint)
    return turned

def turn90(pattern):
    turned = []
    for point in pattern:
        newpoint = dict(xstep = point['ystep'], 
                        ystep = -point['xstep'])
        turned.append(newpoint)
    return turned

def turn180(pattern):
    return turn90(turn90(pattern))

B3 = {
        'pattern' : turn90(centersection),
        'startX'  : 105,
        'startY'  : 37
}

B2 = {
        'pattern' : turn180(centersection),
        'startX'  : 37,
        'startY'  : 37
}

C2 = {
        'pattern' : turnMinus90(centersection),
        'startX'  : 37,
        'startY'  : 105
}

C3 = {
        'pattern' : centersection,
        'startX'  : 105,
        'startY'  : 105
}

A3 = {
        'pattern' : section1,
        'startX'  : 105,
        'startY'  : 31
}

A2 = {
        'pattern' : section1,
        'startX'  : 67,
        'startY'  : 31
}

B1 = {
        'pattern' : turn90(section1),
        'startX'  : 31,
        'startY'  : 37
}

A1 = {
        'pattern' : corner,
        'startX'  : 31,
        'startY'  : 31
}

C1 = {
        'pattern' : turn90(corner),
        'startX'  : 31,
        'startY'  : 73
}

X = {
        'pattern' : center,
        'startX'  : 67,
        'startY'  : 76
}
sections = [
    C3, C2, B2, B3, A3, A2, B1, A1, C1, X
]

#~ print section1
