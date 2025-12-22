import pytest
import numpy as np
import Model as model

Video = model.Video
Model = model.Model
View = model.View
defaultParameters = model.defaultParameters


class FakeCapture:
    """A small fake replacement for cv2.VideoCapture used in tests."""
    def __init__(self, frames=None, width=640, height=480, fps=30):
        self._frames = frames or []
        self._i = 0
        self._width = width
        self._height = height
        self._fps = fps

    def get(self, prop):
        if prop == model.cv.CAP_PROP_FRAME_WIDTH:
            return self._width
        if prop == model.cv.CAP_PROP_FRAME_HEIGHT:
            return self._height
        if prop == model.cv.CAP_PROP_FPS:
            return self._fps
        return 0

    def read(self):
        if self._i < len(self._frames):
            f = self._frames[self._i]
            self._i += 1
            return True, f
        return False, None


class DummyVideo:
            def __init__(self, frame, points):
                self.frame = frame
                self.points = points
                self.marked = False
                self.incremented = False

            def getCurrentFrame(self):
                return self.frame

            def getPoints(self):
                return self.points

            def markFirstFrame(self):
                self.marked = True

            def incrementFrame(self):
                self.incremented = True
                return True


class TestVideo:
    def testConstructor(self):
        fake = FakeCapture()
        video = Video("dummy.mp4", (255, 0, 0))
        assert video._video is not None
        assert video._ballColour == (255, 0, 0)
        assert video._curFrame is None
        assert video._firstValidFrame is None
        assert video._frames == []
        assert video._points == []
        assert video._params == defaultParameters()
    
    def testGetDimensionsAndFPS(self):
        fake = FakeCapture(width=800, height=600, fps=24)
        video = Video("dummy.mp4", (255, 0, 0))
        video._video = fake  # Inject our fake capture

        assert video.getDimensions() == (800, 600)
        assert video.getFPS() == 24
    
    def testMarkFirstFrame(self):
        video = Video("dummy.mp4", (255, 0, 0))
        assert video.markFirstFrame() is False  # No frames yet

        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        video._frames.append(frame)
        assert video.markFirstFrame() is True
        assert video._firstValidFrame == 0
    
    def testIncrementFrameNoFrame(self):
        fake = FakeCapture(frames=[])
        video = Video("none.mp4", (0, 0, 0))
        video._video = fake  # Inject our fake capture
        assert video.incrementFrame() is False
        assert video._curFrame is None
    
    def testIncrementFrameWithFrame(self):
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.ones((100, 100, 3), dtype=np.uint8) * 255
        fake = FakeCapture(frames=[frame1, frame2])
        video = Video("some.mp4", (0, 0, 0))
        video._video = fake  # Inject our fake capture

        assert video.incrementFrame() is True
        np.testing.assert_array_equal(video._curFrame, frame1)

        assert video.incrementFrame() is True
        np.testing.assert_array_equal(video._curFrame, frame2)

        assert video.incrementFrame() is False  # No more frames

