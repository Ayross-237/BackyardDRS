import cv2 as cv
import tkinter as tk
from tkinter import messagebox
from library import *
from PIL import Image, ImageTk

class FrameElement:
    def __init__(self, root):
        self._frame = tk.Frame(root)
    
    def getFrame(self) -> tk.Frame:
        return self._frame

class VideoView:
    """
    A class to handle the video display in a Tkinter GUI.
    """
    def __init__(self, root, width, height):
        """
        Initializes the VideoView object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        self._width = width
        self._height = height
        self._root = root
        self._label = tk.Label(root)
    
    def getLabel(self):
        """
        Returns the label containing the video frame.
        """
        return self._label

    def updateFrame(self, frame, circles=[], cropRegion=None):
        """
        Updates the displayed frame in the GUI.
        parameters:
            frame: The frame to display (as a numpy array).
        """
        for circle in circles:
            cv.circle(frame, (circle[0], circle[1]), circle[2], (0, 0, 255), 2)
        if cropRegion is not None:
            cv.rectangle(frame, cropRegion[0], cropRegion[1], (255, 255, 255), 2)
        
        frame = cv.resize(frame, (self._width, self._height), interpolation=cv.INTER_AREA)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self._label.imgtk = imgtk 
        self._label.configure(image=imgtk)


class Slider:
    def __init__(self, root: tk.Frame, label: str, from_:float, to: float, resolution: float, default: float, orient=tk.VERTICAL):
        """
        Initializes the Slider object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
            label: The label for the slider.
            from_: The minimum value of the slider.
            to: The maximum value of the slider.
            orient: The orientation of the slider (default is HORIZONTAL).
        """
        self._root = root
        self._frame = tk.Frame(root)

        self._label = tk.Label(self._frame, text=label)
        self._label.pack(side=tk.TOP, fill=tk.X, expand=tk.TRUE)
        self._scale = tk.Scale(self._frame, orient=orient, length=100, from_=from_, to=to, resolution=resolution)
        self._scale.set(default)
        self._scale.pack(side=tk.TOP)
        

    def getFrame(self):
        """
        Returns the frame containing the slider.
        """
        return self._frame
    
    def getValue(self):
        """
        Returns the current value of the slider.
        """
        return self._scale.get()

    def onChange(self, function):
        """
        Sets a function to be called when the slider value changes.
        parameters:
            function: The function to call when the slider value changes.
        """
        self.function = function
        self._scale.bind("<ButtonRelease-1>", self._updateParameters)
    
    def _updateParameters(self, event):
        self.function()


class ParameterBar:
    """
    A class to handle the parameter bar in a Tkinter GUI.
    """
    PARAMETERS = [
        (Parameter.BLUR_SQR_SIZE, 1, 33, 2),
        (Parameter.DP, 0.5, 2.0, 0.01),
        (Parameter.MIN_DIST, 1, 500, 1),
        (Parameter.MIN_RADIUS, 1, 100, 1),
        (Parameter.MAX_RADIUS, 1, 100, 1),
        (Parameter.PARAM1, 1, 300, 1),
        (Parameter.PARAM2, 1, 300, 1)
    ]

    def __init__(self, root, parameters: Parameters, function):
        """
        Initializes the ParameterBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        self._root = root
        self._frame = tk.Frame(root)
        self._sliders = {} 

        def onChange():
            function(self.getParameters())

        for param, from_, to, step in self.PARAMETERS:
            slider = Slider(self._frame, param.value, from_, to, step, (to + from_) / 2)
            slider.onChange(lambda: onChange())
            slider.getFrame().pack(side=tk.LEFT, expand=tk.Y)
            self._sliders[param] = slider
    
    def getFrame(self):
        """
        Returns the frame containing the parameter bar.
        """
        return self._frame
    
    def addSlider(self, label: str, from_:float, to: float, default: float, orient=tk.HORIZONTAL, function=None) -> None:
        """
        Adds a slider to the parameter bar.
        parameters:
            label: The label for the slider.
            from_: The minimum value of the slider.
            to: The maximum value of the slider.
            orient: The orientation of the slider (default is HORIZONTAL).
        """
        slider = Slider(self._frame, label, from_, to, default, orient)
        if function is not None:
            slider.onChange(function)
        slider.getFrame().pack(side=tk.LEFT, expand=tk.Y)
    
    def getParameters(self) -> Parameters:
        """
        Returns the current parameters from the sliders.
        returns:
            Parameters: The current parameters.
        """
        return Parameters(
            blurSqrSize=int(self._sliders[Parameter.BLUR_SQR_SIZE].getValue()),
            dp=float(self._sliders[Parameter.DP].getValue()),
            minDist=int(self._sliders[Parameter.MIN_DIST].getValue()),
            minRadius=int(self._sliders[Parameter.MIN_RADIUS].getValue()),
            maxRadius=int(self._sliders[Parameter.MAX_RADIUS].getValue()),
            param1=int(self._sliders[Parameter.PARAM1].getValue()),
            param2=int(self._sliders[Parameter.PARAM2].getValue())
        )

class CropControlBar:
    def __init__(self, root, videoDimensions, setCropFunction):
        """
        Initializes the CropControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        self._root = root
        self._frame = tk.Frame(root)

        self._setCropFunction = setCropFunction

        self._top = Slider(self._frame, "Top", 0, videoDimensions[1], 1, 0)
        self._top.getFrame().pack(side=tk.LEFT)
        self._left = Slider(self._frame, "Left", 0, videoDimensions[0], 1, 0)
        self._left.getFrame().pack(side=tk.LEFT)
        self._bottom = Slider(self._frame, "Bottom", 0, videoDimensions[1], 1, videoDimensions[1])
        self._bottom.getFrame().pack(side=tk.LEFT)
        self._right = Slider(self._frame, "Right", 0, videoDimensions[0], 1, videoDimensions[0])
        self._right.getFrame().pack(side=tk.LEFT)

        def crop():
            try:
                left = int(self._left.getValue())
                top = int(self._top.getValue())
                right = int(self._right.getValue())
                bottom = int(self._bottom.getValue())
                self._setCropFunction((left, top), (right, bottom))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid integer values for crop coordinates.")

        self._top.onChange(crop)
        self._left.onChange(crop)
        self._bottom.onChange(crop)
        self._right.onChange(crop)
    
    def getFrame(self):
        """
        Returns the frame containing the crop control bar.
        """
        return self._frame


class PlaybackBar:
    def __init__(self, root, nextFunction, startTrackFunction):
        """
        Initializes the VideoControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        self._root = root
        self._frame = tk.Frame(root)

        nextButton = tk.Button(self._frame, text="Next Frame", command=nextFunction)
        nextButton.pack(side=tk.LEFT)

        trackButton = tk.Button(self._frame, text="Start Tracking", command=startTrackFunction)
        trackButton.pack(side=tk.LEFT)
    
    def getFrame(self):
        """
        Returns the frame containing the video control bar.
        """
        return self._frame


class VideoControlBar:
    def __init__(self, root, videoName, dimensions, parameterFunction, cropFunction, nextFunction, startTrackFunction):
        """
        Initializes the ControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        self._root = root
        self._frame = tk.Frame(root)
        label = tk.Label(self._frame, text=videoName, font=("Arial", 16), bg="lightgrey", fg="black")
        label.pack(side=tk.TOP, fill=tk.X, expand=tk.TRUE)

        parameterFrame = tk.Frame(self._frame)
        parameterLabel = tk.Label(parameterFrame, text="Parameters:", font=("Arial", 12))
        parameterLabel.pack(side=tk.TOP, fill=tk.X)
        parameterBar = ParameterBar(parameterFrame, defaultParameters(), parameterFunction)
        parameterBar.getFrame().pack(side=tk.TOP, fill=tk.X)
        parameterFrame.pack(side=tk.LEFT, fill=tk.X, padx=25)

        cropFrame = tk.Frame(self._frame)
        cropLabel = tk.Label(cropFrame, text="Crop Region:", font=("Arial", 12))
        cropLabel.pack(side=tk.TOP, fill=tk.X)
        cropBar = CropControlBar(cropFrame, dimensions, cropFunction)
        cropBar.getFrame().pack(side=tk.TOP, fill=tk.X)
        cropLabel.pack(side=tk.TOP, fill=tk.X)
        cropFrame.pack(side=tk.LEFT, fill=tk.X, padx=25)

        playbackFrame = tk.Frame(self._frame)
        playbackLabel = tk.Label(playbackFrame, text="Playback Controls:", font=("Arial", 12))
        playbackLabel.pack(side=tk.TOP, fill=tk.X)
        playbackBar = PlaybackBar(playbackFrame, nextFunction, startTrackFunction)
        playbackBar.getFrame().pack(side=tk.TOP, fill=tk.BOTH)
        playbackFrame.pack(side=tk.LEFT, fill=tk.X, padx=25)

    
    def getFrame(self):
        """
        Returns the frame containing the control bar.
        """
        return self._frame

class MasterControlBar:
    def __init__(self, root, makePredictionFunction, linkFunction):
        """
        Initializes the MasterControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        self._root = root
        self._frame = tk.Frame(root)

        predictButton = tk.Button(self._frame, text="Make Prediction", command=makePredictionFunction)
        predictButton.pack(side=tk.LEFT)

        linkButton = tk.Button(self._frame, text="Link Videos", command=linkFunction)
        linkButton.pack(side=tk.LEFT)
    
    def getFrame(self):
        """
        Returns the frame containing the master control bar.
        """
        return self._frame
