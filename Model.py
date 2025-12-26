import cv2 as cv
import numpy as np
from scipy.optimize import curve_fit
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
        self._cropRegion = ((0, 0), self.getDimensions())
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
    
    def getCropRegion(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Returns the current crop region for the video frames.

        returns:
            tuple[tuple[int, int], tuple[int, int]]: Top-left and bottom-right coordinates of the crop region.
        """
        return self._cropRegion
    
    def cropToRegion(self, topLeft: tuple[int, int], bottomRight: tuple[int, int]) -> None:
        """
        Sets the crop region for the video frames.

        parameters:
            topLeft (tuple[int, int]): Top-left coordinates of the crop region.
            bottomRight (tuple[int, int]): Bottom-right coordinates of the crop region.
        """
        self._cropRegion = (topLeft, bottomRight)
        self._recalculatePoints()

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
        if prevCircle:
            prevCircle = (prevCircle[0] - self._cropRegion[0][0], prevCircle[1] - self._cropRegion[0][1], prevCircle[2], prevCircle[3])


        # Split the frame into its color channels and apply Gaussian blur
        cropped = self._curFrame[self._cropRegion[0][1]:self._cropRegion[1][1], self._cropRegion[0][0]:self._cropRegion[1][0]]
        b, g, r = cv.split(cropped)
        blur = cv.GaussianBlur(r, (self._params.blurSqrSize, self._params.blurSqrSize), 0)

        # Detect circles in the blurred image using HoughCircles
        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 
            self._params.dp, 
            self._params.minDist, 
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
        
        # Account for the fact that only a cropped image is used in the algorithm
        adjustedX = chosen[0] + self._cropRegion[0][0]
        adjustedY = chosen[1] + self._cropRegion[0][1]
        chosen = (adjustedX, adjustedY, chosen[2], len(self._frames))
        self._points.append(chosen)
        
    def updateParameters(self, params: Parameters) -> None:
        """
        Updates the ball tracking parameters.

        parameters:
            params (Parameters): New ball tracking parameters.
        """
        self._params = params
        self._points = []
        self._recalculatePoints()
    
    def _recalculatePoints(self) -> None:
        """
        Recalculates all tracked ball positions based on the current parameters.
        """
        self._points = []
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
    
    def startTracking(self, view: View) -> bool:
        """
        Starts the ball tracking process for both video views.
        """
        if self._isLinked:
            return self._frontVideo.markFirstFrame() and self._sideVideo.markFirstFrame()
        elif view == View.FRONT:
            return self._frontVideo.markFirstFrame()
        elif view == View.SIDE:
            return self._frontVideo.markFirstFrame()
        return False
    
    def render(self) -> dict[View, Render]:
        """
        Renders the current frames and ball tracking points from both video views.

        returns:
            Render: A Render object containing the current frames and ball tracking points.
        """
        frontRender = Render(
            frame=self._frontVideo.getCurrentFrame(),
            circles=self._frontVideo.getPoints(),
            cropRegion=self._frontVideo.getCropRegion(),
            verticalLines=[]
        )
        sideRender = Render(
            frame=self._sideVideo.getCurrentFrame(),
            circles=self._sideVideo.getPoints(),
            cropRegion=self._sideVideo.getCropRegion(),
            verticalLines=[self._stumpPosition] if self._stumpPosition is not None else []
        )
        return {View.FRONT: frontRender, View.SIDE: sideRender}

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
            if self._framesSinceLink[fast] > FPSRatio * self._framesSinceLink[slow]:
                slow.incrementFrame()
                self._framesSinceLink[slow] += 1
        elif view == View.FRONT:
            return self._frontVideo.incrementFrame()
        elif view == View.SIDE:
            return self._sideVideo.incrementFrame()
        return False
    
    def cropRegion(self, view: View, topLeft: tuple[int, int], bottomRight: tuple[int, int]) -> None:
        """
        Sets the crop region for the specified video view.

        parameters:
            view (View): The video view to crop (FRONT or SIDE).
            topLeft (tuple[int, int]): Top-left coordinates of the crop region.
            bottomRight (tuple[int, int]): Bottom-right coordinates of the crop region.
        """
        if view == View.FRONT:
            self._frontVideo.cropToRegion(topLeft, bottomRight)
        elif view == View.SIDE:
            self._sideVideo.cropToRegion(topLeft, bottomRight)
        
    def updateParameters(self, view: View, params: Parameters) -> None:
        """
        Updates the ball tracking parameters for the specified video view.

        parameters:
            view (View): The video view to update (FRONT or SIDE).
            params (Parameters): New ball tracking parameters.
        """
        if view == View.FRONT:
            self._frontVideo.updateParameters(params)
        elif view == View.SIDE:
            self._sideVideo.updateParameters(params)
    
    def markFirstFrame(self, view: View) -> bool:
        """
        Starts tracking the ball in the specified video view.

        parameters:
            view (View): The video view to start tracking (FRONT or SIDE).
        """
        if view == View.FRONT:
            return self._frontVideo.markFirstFrame()
        elif view == View.SIDE:
            return self._sideVideo.markFirstFrame()
        return False

    def makePrediction(self) -> tuple[int]:
        """
        Outputs the predicted line and height of the ball from the data collected from ball tracking.
        """

        if self._stumpPosition == None:
            raise ValueError("Stump position must be set.")
        if self._isLinked == False:
            raise ValueError("Must link videos before predicting.")
        if len(self._frontVideo.getPoints()) < 2 or len(self._sideVideo.getPoints()) < 3:
            raise ValueError("Not enough points to make prediction.")
        
        numFrames = self._requiredFramesForPrediction()
        line = self._predictLine(int(numFrames * self._frontVideo.getFPS() / self._sideVideo.getFPS()))
        height = self._predictHeight(numFrames)
        print(line, height)
        return (line, height)

    def _requiredFramesForPrediction(self) -> int:
        """
        Returns the number of frames required from the side video to make a prediction.
        """
        sidePoints = self._sideVideo.getPoints()
        xs = [sidePoints[i][0] for i in range(len(sidePoints))]
        frames = [sidePoints[i][3] for i in range(len(sidePoints))]

        if len(xs) < 2:
            raise ValueError("Not enough points to make a prediction.")

        lineParams, _ = curve_fit(linear, frames, xs)
        predictedFrames = linearInverse([self._stumpPosition], *lineParams)
        return predictedFrames[0] - frames[-1]

    def _predictLine(self, numFrames: int) -> int:
        """
        Returns the predicted line of the ball as viewed from the front angle, giving the expected vertical line
        """
        frontPoints = self._frontVideo.getPoints()
        bounce = self._findBounceFrame(frontPoints)
        xs = [frontPoints[i][0] for i in range(bounce, len(frontPoints))]
        frames = [frontPoints[i][3] for i in range(bounce, len(frontPoints))]

        if len(xs) < 2:
            raise ValueError("Not enough points after bounce to make line prediction.")
    
        lineParams, _ = curve_fit(linear, frames, xs)
        prediction = linear([frames[-1] + numFrames], *lineParams)
        return int(prediction[0])
    
    def _predictHeight(self, numFrames: int) -> int:
        """
        Returns the predicted height of the ball as viewed from the side angle, giving the expected height above ground.
        """
        sidePoints = self._sideVideo.getPoints()
        bounce = self._findBounceFrame(sidePoints)
        ys = [sidePoints[i][1] for i in range(bounce, len(sidePoints))]
        frames = [sidePoints[i][3] for i in range(bounce, len(sidePoints))]

        if len(ys) < 3:
            raise ValueError("Not enough points to make height prediction.")
        
        heightParams, _ = curve_fit(quadratic, frames, ys)
        prediction = quadratic([frames[-1] + numFrames], *heightParams)
        return int(prediction[0])
    
    def _findBounceFrame(self, points: list[list[int]]) -> int:
        """
        Finds the first frame after the ball bounce based on the tracked points.

        parameters:
            points (list[list[int]]): List of tracked ball positions.
        """
        for i in range(1, len(points)-1):
            if points[i][1] > points[i-1][1] and points[i][1] > points[i+1][1]:
                return i
        return 0

