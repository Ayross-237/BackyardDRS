import cv2 as cv

class Video:
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

    