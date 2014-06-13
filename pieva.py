import svg.path
import numpy as np

section1path = svg.path.parse_path("m 2549.3832,2630.459 -237.2217,-246.2302 234.2189,-234.2189 84.0786,-231.2162 -3.0028,-315.2947 -237.2217,231.2161 -237.2218,249.233 -234.219,234.219 -228.2133,222.2077 -234.219,84.0786 -75.0701,-231.2161 237.2217,-243.2274 231.2162,-228.2134 231.2161,-228.2133 225.2106,-240.2246 240.2245,-231.2161 84.0786,-240.22458 -237.2217,-72.06737 -240.2246,243.22735 -234.219,231.2162 -234.2189,228.2133 -231.2162,240.2246 -228.2133,225.2105 -243.22738,231.2162 -231.21614,243.2273 -228.21334,75.0702 -234.21896,-84.0786 234.21896,-231.2161 237.22176,-231.2162 228.21334,-231.2161 237.22176,-234.219 231.2161,-240.2245 231.2162,-231.2162 222.2077,-237.22176 252.2358,-231.21614 231.2162,-225.21054 -81.0758,-234.21895 -231.2162,72.06737 -234.2189,237.22176 -249.233,231.21615 -225.2106,225.21053 -231.2161,243.22738 -237.22176,243.2274 -228.21334,231.2161 -249.23299,228.2134 -222.20773,228.2133 0,-315.2947 L 294.2751,1612.5074 519.48563,1372.2828 750.70178,1144.0695 993.92915,900.84213 1234.1537,672.62879 1447.353,447.41826 1387.2969,216.20211 1156.0807,288.26948 900.46678,520.98703 679.38511,758.58414 441.41264,987.92353 209.07045,1227.022 216.20211,906.84774 285.26667,675.6316 525.49124,438.40983 288.26948,207.19369")
cornerpath = svg.path.parse_path("m 2547.8818,2628.9576 -241.7259,-240.2246 243.2273,-229.7147 76.5716,-235.7204 -1.5014,-312.2919 -231.2161,232.7176 -235.7204,232.7175 -232.7175,237.2218 -237.2218,235.7203 -232.7176,76.5716 -75.0701,-234.2189 235.7203,-235.7204 231.2162,-225.2105 237.2217,-241.726 229.7148,-234.219 232.7175,-229.7147 84.0786,-232.71756 -4.5042,-316.79615 -229.7147,231.21615 -235.7204,238.72316 -234.2189,232.7176 -240.2246,234.2189 -234.219,235.7204 -229.7147,237.2217 -235.72037,228.2134 -234.21895,232.7175 -235.72036,81.0758 -234.21895,-79.5744 237.22176,-237.2217 241.72597,-232.7176 219.20492,-229.7147 244.72878,-235.7204 232.7175,-231.2161 231.2162,-241.726 235.7204,-231.21616 234.2189,-237.22176 235.7204,-231.21614 -85.58,-229.71475 -229.7148,79.57439 -229.7147,226.71194 -234.219,237.22176 -234.2189,234.21895 -235.7204,241.72597 -232.71754,228.2133 -240.22457,231.2162 -240.22457,4.5042 93.08702,-235.7204 229.71475,-237.2217 231.21614,-235.72037 241.72597,-231.21615 228.2133,-228.21334 6.0057,-7.50702")
section1 = []
corner=[]

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

A1 = {
        'pattern' : corner,
        'startX'  : 31,
        'startY'  : 31}

A2 = {
        'pattern' : section1,
        'startX'  : 37,
        'startY'  : 31}
A3 = {
        'pattern' : turnMinus90(section1),
        'startX'  : 73,
        'startY'  : 31}
A4 = {
        'pattern' : turnMinus90(corner),
        'startX'  : 109,
        'startY'  : 31}
B1 = {
        'pattern' : section1,
        'startX'  : 31,
        'startY'  : 67}
B2 = {
        'pattern' : section1,
        'startX'  : 67,
        'startY'  : 67}
B3 = {
        'pattern' : turnMinus90(section1),
        'startX'  : 73,
        'startY'  : 67}
B4 = {
        'pattern' : turnMinus90(section1),
        'startX'  : 109,
        'startY'  : 67}
C1 = {
        'pattern' : turn90(section1),
        'startX'  : 31,
        'startY'  : 73}
C2 = {
        'pattern' : turn90(section1),
        'startX'  : 67,
        'startY'  : 73}
C3 = {
        'pattern' : turn180(section1),
        'startX'  : 73,
        'startY'  : 73}
C4 = {
        'pattern' : turn180(section1),
        'startX'  : 109,
        'startY'  : 73}
D1 = {
        'pattern' : turn90(corner),
        'startX'  : 31,
        'startY'  : 109}
D2 = {
        'pattern' : turn90(section1),
        'startX'  : 67,
        'startY'  : 109}
D3 = {
        'pattern' : turn180(section1),
        'startX'  : 73,
        'startY'  : 109}
D4 = {
        'pattern' : turn180(corner),
        'startX'  : 109,
        'startY'  : 109}


sections = [
    B2, C2, C3, B3,
    B1, C1, D2, D3,
    B4, C4, A2, A3,
    A1, D1, D4, A4
]

#~ print section1
