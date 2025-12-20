from dataclasses import dataclass
from enum import Enum

class View(Enum):
    FRONT = 1
    SIDE = 2

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
    frontFrame: any
    sideFrame: any
    frontPoints: list[tuple[int]]
    sidePoints: list[tuple[int]]
    stumpPosition: int | None

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