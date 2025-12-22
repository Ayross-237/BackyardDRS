import cv2 as cv
import numpy as np
from dataclasses import dataclass
from library import *

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
        self._params = defaultParameters()

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

    def getPoints(self) -> list[tuple[int]]:
        """
        Returns a copy of the list of tracked ball positions.
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
        """
        Tracks the ball in the current frame and updates the points list.
        Requires that at least one frame has been processed.
        """
        prevCircle = self._points[-1] if len(self._points) > 0 else None

        # Split the frame into its color channels and apply Gaussian blur
        b, g, r = cv.split(self._curFrame)
        blur = cv.GaussianBlur(r, (self._params.blurSqrSize, self._params.blurSqrSize), 0)

        # Detect circles in the blurred image using HoughCircles
        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, self._params.dp, self._params.minDist, 
            param1=self._params.param1, 
            param2=self._params.param2, 
            minRadius=self._params.minRadius, 
            maxRadius=self._params.maxRadius
        )

        if circles is None:
            return
        
        # Add the most likely circle to the points list based on distance to the previous circle
        circles = np.uint32(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: 
                chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen = i
        self._points.append(chosen[:3])
        
    def updateParameters(self, params: Parameters) -> None:
        """
        Updates the ball tracking parameters.

        parameters:
            params (Parameters): New ball tracking parameters.
        """
        self._params = params
        self._points = []
        print(self._firstValidFrame, len(self._frames))
        if self._firstValidFrame is not None:
            for i in range(self._firstValidFrame, len(self._frames)):
                self._curFrame = self._frames[i]
                self._trackBallInCurrentFrame()
        
class Model:
    """
    A class to handle the ball tracking model.
    """
    def __init__(self, frontVideo: Video, sideVideo: Video) -> None:
        """
        Initializes the Model object with the given video objects.

        parameters:
            frontVideo (Video): Video object for the front view.
            sideVideo (Video): Video object for the side view.
        """
        self._frontVideo = frontVideo
        self._sideVideo = sideVideo
        self._isLinked = False
        self._stumpPosition = None
        self._framesSinceLink = {frontVideo: 0, sideVideo: 0}
    
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

    def incrementFrame(self, view: View) -> bool:
        """
        Advances to the next frame in the specified video view.

        parameters:
            view (View): The video view to increment (FRONT or SIDE).

        returns:
            bool: True if successful, false otherwise.
        """
        if self._isLinked:
            FPSRatio = self._frontVideo.getFPS() / self._sideVideo.getFPS()
            fast, slow = self._frontVideo, self._sideVideo
            if FPSRatio < 1:
                fast, slow = self._sideVideo, self._frontVideo
                FPSRatio = 1 / FPSRatio
            
            fast.incrementFrame()
            self._framesSinceLink[fast] += 1
            if self._framesSinceLink[fast] / self._framesSinceLink[slow] < FPSRatio:
                slow.incrementFrame()
                self._framesSinceLink[slow] += 1

        if view == View.FRONT:
            return self._frontVideo.incrementFrame()
        elif view == View.SIDE:
            return self._sideVideo.incrementFrame()
        return False