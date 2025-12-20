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


class TestModel:
    def test_get_dimensions_and_fps_and_markFirstFrame(monkeypatch):
        fake = FakeCapture(frames=[])
        monkeypatch.setattr(model.cv, 'VideoCapture', lambda path: fake)
        v = Video("dummy.mp4", (255, 0, 0))

        assert v.getDimensions() == (fake._width, fake._height)
        assert v.getFPS() == fake._fps

        # no frames yet
        assert v.markFirstFrame() is False

        # add a frame and mark
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        v._frames.append(frame)
        assert v.markFirstFrame() is True
        assert v._firstValidFrame == 0


    def test_incrementFrame_no_frame(monkeypatch):
        fake = FakeCapture(frames=[])
        monkeypatch.setattr(model.cv, 'VideoCapture', lambda path: fake)
        v = Video("none.mp4", (0, 0, 0))
        assert v.incrementFrame() is False


    def test_incrementFrame_with_tracking(monkeypatch):
        # single frame that will be "detected" as a circle by patched HoughCircles
        frame = np.zeros((200, 200, 3), dtype=np.uint8)
        fake = FakeCapture(frames=[frame])
        monkeypatch.setattr(model.cv, 'VideoCapture', lambda path: fake)

        # stub HoughCircles to return one circle at (50,50) radius 10
        monkeypatch.setattr(model.cv, 'HoughCircles', lambda *a, **k: np.array([[[50, 50, 10]]]))

        v = Video("track.mp4", (0, 0, 0))
        v._firstValidFrame = 0

        assert v.incrementFrame() is True
        assert len(v._points) == 1
        x, y, r = v._points[0]
        assert int(x) == 50 and int(y) == 50


    def test_updateParameters_retracks(monkeypatch):
        # two frames; ensure updateParameters re-runs tracking on both
        f1 = np.zeros((100, 100, 3), dtype=np.uint8)
        f2 = np.zeros((100, 100, 3), dtype=np.uint8)

        fake = FakeCapture(frames=[])
        monkeypatch.setattr(model.cv, 'VideoCapture', lambda path: fake)
        v = Video("retrack.mp4", (0, 0, 0))

        v._frames = [f1, f2]
        v._firstValidFrame = 0

        # HoughCircles will return a different circle each time it's called
        calls = {'i': 0}

        def hough(blur, *a, **k):
            i = calls['i']
            calls['i'] += 1
            if i == 0:
                return np.array([[[10, 10, 5]]])
            return np.array([[[20, 20, 6]]])

        monkeypatch.setattr(model.cv, 'HoughCircles', hough)

        v.updateParameters(defaultParameters())

        assert len(v._points) == 2
        assert tuple(int(x) for x in v._points[0]) == (10, 10, 5)
        assert tuple(int(x) for x in v._points[1]) == (20, 20, 6)


    def test_model_render_and_increment_and_link():
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

        fv = DummyVideo("front_frame", [(1, 2, 3)])
        sv = DummyVideo("side_frame", [(4, 5, 6)])

        m = Model(fv, sv)
        m.setStumpPosition(42)
        m.linkVideos()

        assert m._isLinked is True

        m.startTracking()
        assert fv.marked is True and sv.marked is True

        r = m.render()
        assert r.frontFrame == "front_frame"
        assert r.sideFrame == "side_frame"
        assert r.frontPoints == [(1, 2, 3)]
        assert r.sidePoints == [(4, 5, 6)]
        assert r.stumpPosition == 42

        assert m.incrementFrame(View.FRONT) is True
        assert fv.incremented is True

        fv.incremented = False
        assert m.incrementFrame(View.SIDE) is True
        assert sv.incremented is True

        # invalid view should return False
        assert m.incrementFrame(None) is False
