import cv2 as cv
import numpy as np
from dataclasses import dataclass

@dataclass
class Render:
    frontFrame: any
    sideFrame: any
    frontPoints: list[tuple[int]]
    sidePoints: list[tuple[int]]
    stumpPosition: int | None

class Video:
    """
    A class to handle video processing and ball tracking.
    """
    def __init__(self, filePath: str, ballColour: tuple[int]) -> None:
        """
        Initializes the Video object with the given parameters.

        parameters:
            filePath (str): Path to the video file.
            ballColour (tuple[int]): RGB color of the ball to track.
            width (int): Width to resize the video frames.
            height (int): Height to resize the video frames.
            fps (int): Frames per second of the video.
        """
        self._video = cv.VideoCapture(filePath)
        self._ballColour = ballColour
        self._curFrame = None
        self._firstValidFrame = None
        self._frames = []
        self._points = []


    def getDimensions(self) -> tuple[int, int]:
        """
        Returns the dimensions of the video frames.

        returns:
            tuple[int, int]: Width and height of the video frames.
        """
        width = int(self._video.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self._video.get(cv.CAP_PROP_FRAME_HEIGHT))
        return (width, height)


    def getFPS(self) -> int:
        """
        Returns the frames per second of the video.

        returns:
            int: Frames per second of the video.
        """
        return int(self._video.get(cv.CAP_PROP_FPS))
    

    def markFirstFrame(self) -> bool:
        """
        Starts tracking the ball in the video.
        """
        if len(self._frames) == 0:
            return False
        self._firstValidFrame = len(self._frames) - 1
        return True


    def getCurrentFrame(self):
        """
        Returns a copy of the current frame being processed.

        returns:
            Current video frame.
        """
        return self._curFrame.copy()


    def getPoints(self):
        """
        TODO: DOCUMENT METHOD AND UPDDATE TYPE HINT
        """
        return self._points.copy()


    def incrementFrame(self) -> bool:
        """
        Advances to the next frame in the video and tracks the ball position if it has passed the 
        first valid tracking frame.

        returns:
            bool: True if successful, false otherwise.
        """
        ret, frame = self._video.read()
        if not ret:
            return False
        
        self._curFrame = frame
        self._frames.append(frame)
        if self._firstValidFrame is not None and len(self._frames) - 1 >= self._firstValidFrame:
            self._trackBallInCurrentFrame()
        return True
    
    def _trackBallInCurrentFrame(self) -> None:
        pass



class Model:
    """
    A class to handle the ball tracking model.
    """
    def __init__(self, frontViddeo: Video, sideVideo: Video) -> None:
        """
        Initializes the Model object with the given video objects.

        parameters:
            frontVideo (Video): Video object for the front view.
            sideVideo (Video): Video object for the side view.
        """
        self._frontVideo = frontViddeo
        self._sideVideo = sideVideo
        self._isLinked = False
        self._stumpPosition = None
    

    def setStumpPosition(self, position: int) -> None: 
        """
        Sets the stump position from the view of the side video.

        parameters:
            position (int): The stump position.
        """
        self._stumpPosition = position


    def linkVideos(self) -> bool:
        """
        Links the front and side video views for synchronized ball tracking.

        returns:
            bool: True if linking was successful, false otherwise.
        """
        self._isLinked = True
    

    def startTracking(self) -> None:
        """
        Starts the ball tracking process for both video views.
        """
        self._frontVideo.markFirstFrame()
        self._sideVideo.markFirstFrame()
    

    def render(self) -> Render:
        """
        Renders the current frames and ball tracking points from both video views.

        returns:
            Render: A Render object containing the current frames and ball tracking points.
        """
        frontFrame = self._frontVideo.getCurrentFrame()
        sideFrame = self._sideVideo.getCurrentFrame()
        frontPoints = self._frontVideo.getPoints()
        sidePoints = self._sideVideo.getPoints()
        return Render(frontFrame, sideFrame, frontPoints, sidePoints, self._stumpPosition)
        
    