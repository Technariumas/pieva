
O = dict(xstep = 0, ystep = 0)
W = dict(xstep = -1, ystep = 0)
E = dict(xstep = 1, ystep = 0)
N = dict(xstep = 0, ystep = -1)
S = dict(xstep = 0, ystep = 1)
NE = dict(xstep = 1, ystep = -1)
SE = dict(xstep = 1, ystep = 1)
NW = dict(xstep = -1, ystep = -1)
SW = dict(xstep = -1, ystep = 1)
NEE = dict(xstep = 2, ystep = -1)
SEE = dict(xstep = 2, ystep = 1)
NWW = dict(xstep = -2, ystep = -1)
SWW = dict(xstep = -2, ystep = 1)

square = [
    O, W, W, W, W, W, W, W,
    N, E, E, E, E, E, E, E, 
    N, W, W, W, W, W, W, W,
    N, E, E, E, E, E, E, E, 
    N, W, W, W, W, W, W, W,
    N, E, E, E, E, E, E, E, 
    N, W, W, W, W, W, W, W,
    N, E, E, E, E, E, E, E
] 

topLeftCorner = [
    O, W, W, W, W, W, W, W,
    N, E, E, E, E, E, E, E, 
    N, W, W, W, W, W, W, W,
   NE, E, E, E, E, E, E, 
    N, W, W, W, W, W, W, 
  NEE, E, E, E, E, 
    N, W, W, W, W,  
  NEE, E, E
]

topRightCorner = [
    O, E, E, E, E, E, E, E, 
    N, W, W, W, W, W, W, W,
    N, E, E, E, E, E, E, E, 
   NW, W, W, W, W, W, W, 
    N, E, E, E, E, E, E, 
  NWW, W, W, W, W,  
    N, E, E, E, E, 
  NWW, W, W
]

botLeftCorner = [
    O, W, W, W, W, W, W, W,
    S, E, E, E, E, E, E, E, 
    S, W, W, W, W, W, W, W,
   SE, E, E, E, E, E, E, 
    S, W, W, W, W, W, W, 
  SEE, E, E, E, E, 
    S, W, W, W, W,  
  SEE, E, E
]

botRightCorner = [
    O, E, E, E, E, E, E, E, 
    S, W, W, W, W, W, W, W,
    S, E, E, E, E, E, E, E, 
   SW, W, W, W, W, W, W, 
    S, E, E, E, E, E, E, 
  SWW, W, W, W, W,  
    S, E, E, E, E, 
  SWW, W, W
]

sections = [
        #B2
        {
         'pattern' : square,
         'startX'  : 15,
         'startY'  : 15},
        #C2 
        {
         'pattern' : square,
         'startX'  : 23,
         'startY'  : 15},
        #B3
        {
         'pattern' : square,
         'startX'  : 15,
         'startY'  : 23},
        #C3
        {
         'pattern' : square,
         'startX'  : 23,
         'startY'  : 23},
        #A1
        {
         'pattern' : topLeftCorner,
         'startX'  : 7,
         'startY'  : 7},
        #A2
        {
         'pattern' : square,
         'startX'  : 7,
         'startY'  : 15},
        #A3
        {
         'pattern' : square,
         'startX'  : 7,
         'startY'  : 23},
        #A4
        {
         'pattern' : botLeftCorner,
         'startX'  : 7,
         'startY'  : 24},
        #B1
        {
         'pattern' : square,
         'startX'  : 15,
         'startY'  : 7},
        #B4
        {
         'pattern' : square,
         'startX'  : 15,
         'startY'  : 31},
#---
        #D1
        {
         'pattern' : topRightCorner,
         'startX'  : 24,
         'startY'  : 7},
        #D2
        {
         'pattern' : square,
         'startX'  : 31,
         'startY'  : 15},
        #D3
        {
         'pattern' : square,
         'startX'  : 31,
         'startY'  : 23},
        #D4
        {
         'pattern' : botRightCorner,
         'startX'  : 24,
         'startY'  : 24},
        #C1
        {
         'pattern' : square,
         'startX'  : 23,
         'startY'  : 7},
        #C4
        {
         'pattern' : square,
         'startX'  : 23,
         'startY'  : 31}
]
