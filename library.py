from dataclasses import dataclass
from enum import Enum

class View(Enum):
    FRONT = 1
    SIDE = 2

class Parameter(Enum):
    BLUR_SQR_SIZE = "Blur Square Size"
    DP = "DP"
    MIN_DIST = "Min Distance"
    MIN_RADIUS = "Min Radius"
    MAX_RADIUS = "Max Radius"
    PARAM1 = "Param1"
    PARAM2 = "Param2"

@dataclass
class Parameters:
    blurSqrSize: int
    dp: float
    minDist: int
    minRadius: int
    maxRadius: int
    param1: int
    param2: int

@dataclass
class Render:
    frame: any
    circles: list[tuple[int, int, int]] = ()
    cropRegion: tuple[tuple[int, int], tuple[int, int]] = None
    verticalLines: tuple[int] = ()
    horizontalLines: list[int] = ()


@dataclass
class Callbacks:
    incrementFrame: callable
    updateParameters: callable
    cropRegion: callable
    startTracking: callable
    setStumpPosition: callable
    makePrediction: callable
    linkVideos: callable

def defaultParameters() -> Parameters:
    """
    Returns a Parameters object with default values for ball tracking.

    returns:
        Parameters: A Parameters object with default values.
    """
    return Parameters(
        blurSqrSize=11,
        dp=1.2,
        minDist=100,
        minRadius=10,
        maxRadius=30,
        param1=100,
        param2=30
    )

dist = lambda x1,x2,y1,y2: (x1-x2)**2 + (y1-y2)**2

def linear(xs: list[float], m: float, c: float) -> list[float]:
    return [m*x + c for x in xs]

def linearInverse(ys: list[float], m: float, c: float) -> list[float]:
    return [(y - c) / m for y in ys]

def quadratic(xs: list[float], a: float, b: float, c: float) -> list[float]:
    return [a*(x**2) + b*x + c for x in xs]