import numpy as np
from scipy.optimize import curve_fit
from pylab import *
from math import *

def axis(xs, m, c): # position functions to be used in x and y directions
    out = []
    for x in xs:
        out.append(m*x + c)
    return out

def axis_inv(y, m, c):
    return (y-c)/m

def vert(xs, a, b, c): # position functions to be used in x and y directions
    out = []
    for x in xs:
        out.append(a*x**2 + b*x + c)
    return out

def depth(x, a, c): # depth function of the ball
    y = a/x + c
    return y 

def depth_inv(y, a, c):
    return a / (y-c)