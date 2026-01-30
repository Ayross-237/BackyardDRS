import cv2 as cv
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from library import *
from PIL import Image, ImageTk


class FileChooser(tk.Frame):
    """
    A Tkinter frame that allows the user to choose a file path.
    """
    def __init__(self, root: tk.Tk, label_text: str) -> None:
        """
        Initializes the FileChooser frame.
        Args:
            root (tk.Tk): The Tkinter root window.
            label_text (str): The text for the label.
        """
        super().__init__(root)

        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.TOP, pady=5, expand=True, fill=tk.X)

        self._entry = tk.Entry(self, width=50)
        self._entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.browse_button = tk.Button(self, text="Browse", command=self._browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

    def _browse_file(self) -> None:
        """
        Opens a file dialog to select a file and updates the entry with the selected file path.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self._entry.delete(0, tk.END)
            self._entry.insert(0, file_path)
    
    def getFilePath(self) -> str:
        """
        Returns the file path from the entry.
        """
        return self._entry.get()


class BallColourSlider(tk.Frame):
    """
    A Tkinter frame that contains three sliders for selecting RGB values.
    """
    def __init__(self, root: tk.Tk, label_text: str) -> None:
        """
        Initializes the BallColourSlider frame.
        Args:
            root (tk.Tk): The Tkinter root window.
            label_text (str): The text for the label.
        """
        super().__init__(root)

        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.TOP, pady=5, expand=True, fill=tk.X)

        self.red_slider = tk.Scale(self, from_=0, to=255, resolution=1, orient=tk.VERTICAL, label="Red", length=75)
        self.red_slider.pack(side=tk.LEFT, padx=5, pady=5)

        self.green_slider = tk.Scale(self, from_=0, to=255, resolution=1, orient=tk.VERTICAL, label="Green", length=75)
        self.green_slider.pack(side=tk.LEFT, padx=5, pady=5)

        self.blue_slider = tk.Scale(self, from_=0, to=255, resolution=1, orient=tk.VERTICAL, label="Blue", length=75)
        self.blue_slider.pack(side=tk.LEFT, padx=5, pady=5)

    def getColour(self) -> tuple[int]:
        """
        Returns the selected RGB colour as a tuple.
        """
        return (self.red_slider.get(), self.green_slider.get(), self.blue_slider.get())


class VideoView(tk.Label):
    """
    A class to handle the video display in a Tkinter GUI.
    """
    def __init__(self, root: tk.Frame | tk.Tk, width: int, height: int) -> None:
        """
        Initializes the VideoView object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
            width: The width of the UI element
            height: The height of the UI element
        """
        super().__init__(root)
        self._width = width
        self._height = height
        self._root = root

    def updateFrame(self, frame, circles: list[tuple[int]]=[], cropRegion: tuple[tuple[int]]=None, verticalLines: list[int]=[], horizontalLines=[]) -> None:
        """
        Updates the displayed frame in the GUI.
        parameters:
            frame: The frame to display (as a numpy array).
            circles: The circles to draw on the image
            cropRegion: The region which will be analysed for ball tracking
        """
        # draw tracked ball positions
        for circle in circles:
            cv.circle(frame, (circle[0], circle[1]), circle[2], (0, 0, 255), 2)
        # draw cropped region
        if cropRegion is not None:
            cv.rectangle(frame, cropRegion[0], cropRegion[1], (255, 255, 255), 2)
        for line in verticalLines:
            cv.line(frame, (line, 0), (line, len(frame)), (0, 0, 255), 3)
        for line in horizontalLines:
            cv.line(frame, (0, line), (len(frame[0]), line), (0, 0, 255), 3)
        
        frame = cv.resize(frame, (self._width, self._height), interpolation=cv.INTER_AREA)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.imgtk = imgtk 
        self.configure(image=imgtk)


class Slider(tk.Frame):
    def __init__(self, root: tk.Frame, label: str, from_:float, to: float, resolution: float, default: float, orient=tk.VERTICAL, length=100) -> None:
        """
        Initializes the Slider object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
            label: The label for the slider.
            from_: The minimum value of the slider.
            to: The maximum value of the slider.
            resolution: The increments of the slider.
            default: The initial value on the slider
            orient: The orientation of the slider (default is HORIZONTAL).
        """
        super().__init__(root)

        self._label = tk.Label(self, text=label)
        self._label.pack(side=tk.TOP, fill=tk.X, expand=tk.TRUE)

        self._scale = tk.Scale(self, orient=orient, length=length, from_=from_, to=to, resolution=resolution)
        self._scale.set(default)
        self._scale.pack(side=tk.TOP)
        
    def setValue(self, value: float) -> None:
        """
        Sets the value of the slider the value provided.
        """
        self._scale.set(value)
    
    def getValue(self) -> float:
        """
        Returns the current value of the slider.
        """
        return self._scale.get()

    def onChange(self, function) -> None:
        """
        Sets a function to be called when the slider value changes.
        parameters:
            function: The function to call when the slider value changes.
        """
        self.function = function
        self._scale.bind("<ButtonRelease-1>", self._updateParameters)
    
    def _updateParameters(self, event) -> None:
        self.function()


class ParameterBar(tk.Frame):
    """
    A class to handle the parameter bar in a Tkinter GUI.
    """
    PARAMETERS = [
        (Parameter.BLUR_SQR_SIZE, 1, 33, 2, 13),
        (Parameter.DP, 0.5, 2.0, 0.01, 1.20),
        (Parameter.MIN_DIST, 1, 500, 1, 100),
        (Parameter.MIN_RADIUS, 1, 100, 1, 5),
        (Parameter.MAX_RADIUS, 1, 100, 1, 35),
        (Parameter.PARAM1, 1, 200, 1, 100),
        (Parameter.PARAM2, 1, 50, 1, 20)
    ]

    def __init__(self, root: tk.Frame | tk.Tk, parameters: Parameters, function):
        """
        Initializes the ParameterBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        super().__init__(root)
        self._sliders = {} 

        def onChange():
            function(self.getParameters())

        for param, from_, to, step, default in self.PARAMETERS:
            slider = Slider(self, param.value, from_, to, step, default)
            slider.onChange(onChange)
            slider.pack(side=tk.LEFT, expand=tk.Y)
            self._sliders[param] = slider
    
    def addSlider(self, label: str, from_:float, to: float, default: float, orient=tk.HORIZONTAL, function=None) -> None:
        """
        Adds a slider to the parameter bar.
        parameters:
            label: The label for the slider.
            from_: The minimum value of the slider.
            to: The maximum value of the slider.
            orient: The orientation of the slider (default is HORIZONTAL).
        """
        slider = Slider(self, label, from_, to, default, orient)
        if function is not None:
            slider.onChange(function)
        slider.pack(side=tk.LEFT, expand=tk.Y)
    
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

class CropControlBar(tk.Frame):
    def __init__(self, root: tk.Frame | tk.Tk, videoDimensions: tuple[int], setCropFunction) -> None:
        """
        Initializes the CropControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
            videoDimensions: The dimensions of the video being controlled
            setCropFunction: The function used to execute the crop on the video
        """
        super().__init__(root)

        self._top = Slider(self, "Top", 0, videoDimensions[1], 1, 0)
        self._top.pack(side=tk.LEFT)
        self._left = Slider(self, "Left", 0, videoDimensions[0], 1, 0)
        self._left.pack(side=tk.LEFT)
        self._bottom = Slider(self, "Bottom", 0, videoDimensions[1], 1, videoDimensions[1])
        self._bottom.pack(side=tk.LEFT)
        self._right = Slider(self, "Right", 0, videoDimensions[0], 1, videoDimensions[0])
        self._right.pack(side=tk.LEFT)

        def crop():
            left = int(self._left.getValue())
            top = int(self._top.getValue())
            right = int(self._right.getValue())
            bottom = int(self._bottom.getValue())

            if bottom < top:
                messagebox.showerror("Invalid Crop", "Bottom crop coordinate must be greater than or equal to top crop coordinate")
                self._bottom.setValue(top)
                bottom = top
            elif right < left:
                messagebox.showerror("Invalid Crop", "Right crop coordinate must be greater than or equal to left crop coordinate")
                self._right.setValue(left)
                right = left
            setCropFunction((left, top), (right, bottom))

        self._top.onChange(crop)
        self._left.onChange(crop)
        self._bottom.onChange(crop)
        self._right.onChange(crop)


class PlaybackBar(tk.Frame):
    def __init__(self, root: tk.Frame | tk.Tk, nextFunction, startTrackFunction) -> None:
        """
        Initializes the VideoControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
            nextFunction: The function that moves to the next frame of the video
            startTrackFunction: The function that initiates ball tracking on the video
        """
        super().__init__(root)

        nextButton = tk.Button(self, text="Next Frame", command=nextFunction)
        nextButton.pack(side=tk.LEFT)

        trackButton = tk.Button(self, text="Start Tracking", command=startTrackFunction)
        trackButton.pack(side=tk.LEFT)


class VideoControlBar(tk.Frame):
    def __init__(self, root: tk.Frame | tk.Tk, videoName: str, dimensions: tuple[int], parameterFunction, cropFunction, nextFunction, startTrackFunction) -> None:
        """
        Initializes the ControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
            videoName: The name of the video this bar controls
            dimensions: The dimensions of the video
            parameterFunction: The function that updates the video's ball tracking parameters
            cropFunction: The function that updates the video's crop region
            startTrackFunction: the function that initiates ball tracking on the video
        """
        super().__init__(root)
        label = tk.Label(self, text=videoName, font=("Arial", 16), bg="lightgrey", fg="black")
        label.pack(side=tk.TOP, fill=tk.X, expand=tk.TRUE)

        parameterFrame = tk.Frame(self)
        parameterLabel = tk.Label(parameterFrame, text="Parameters:", font=("Arial", 12))
        parameterLabel.pack(side=tk.TOP, fill=tk.X)
        parameterBar = ParameterBar(parameterFrame, defaultParameters(), parameterFunction)
        parameterBar.pack(side=tk.TOP, fill=tk.X)
        parameterFrame.pack(side=tk.LEFT, fill=tk.X, padx=25)

        cropFrame = tk.Frame(self)
        cropLabel = tk.Label(cropFrame, text="Crop Region:", font=("Arial", 12))
        cropLabel.pack(side=tk.TOP, fill=tk.X)
        cropBar = CropControlBar(cropFrame, dimensions, cropFunction)
        cropBar.pack(side=tk.TOP, fill=tk.X)
        cropLabel.pack(side=tk.TOP, fill=tk.X)
        cropFrame.pack(side=tk.LEFT, fill=tk.X, padx=25)

        playbackFrame = tk.Frame(self)
        playbackLabel = tk.Label(playbackFrame, text="Playback Controls:", font=("Arial", 12))
        playbackLabel.pack(side=tk.TOP, fill=tk.X)
        playbackBar = PlaybackBar(playbackFrame, nextFunction, startTrackFunction)
        playbackBar.pack(side=tk.TOP, fill=tk.BOTH)
        playbackFrame.pack(side=tk.LEFT, fill=tk.X, padx=25)


class MasterControlBar(tk.Frame):
    def __init__(self, root, makePredictionFunction, linkFunction, setStumpFunction, sideVideoDimensions):
        """
        Initializes the MasterControlBar object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
        """
        super().__init__(root)

        self._stumpFunction = setStumpFunction
        self._stumpSlider = Slider(self, "Stump Position", 0, sideVideoDimensions[0], 1, 0, orient=tk.HORIZONTAL)
        self._stumpSlider.onChange(self._setStumpPos)
        self._stumpSlider.pack(side=tk.LEFT)

        predictButton = tk.Button(self, text="Make Prediction", command=makePredictionFunction)
        predictButton.pack(side=tk.LEFT)

        linkButton = tk.Button(self, text="Link Videos", command=linkFunction)
        linkButton.pack(side=tk.LEFT)

    def _setStumpPos(self) -> None:
        self._stumpFunction(self._stumpSlider.getValue())


class VIEW:
    def __init__(self, root: tk.Tk, frontDimensions: tuple[int], sideDimensions: tuple[int], callbacks: Callbacks) -> None:
        """
        Initializes the VideoView object with the given Tkinter root.
        parameters:
            root: The Tkinter root window.
            width: The width of the UI element
            height: The height of the UI element
        """
        root.title("Backyard DRS")
        
        self._frontView = VideoView(root, 540, 960)
        self._frontView.pack(side=tk.LEFT)

        rightFrame = tk.Frame(root)
        rightFrame.pack(side=tk.LEFT, fill=tk.BOTH)
        
        self._sideView = VideoView(rightFrame, 960, 540)
        self._sideView.pack(side=tk.TOP)

        self._frontControlBar = VideoControlBar(
            rightFrame,
            "Front View",
            frontDimensions,
            lambda params: callbacks.updateParameters(View.FRONT, params),
            lambda topLeft, bottomRight: callbacks.cropRegion(View.FRONT, topLeft, bottomRight),
            lambda: callbacks.incrementFrame(View.FRONT),
            lambda: callbacks.startTracking(View.FRONT)
        )
        self._frontControlBar.pack(side=tk.TOP, fill=tk.X)

        self._sideControlBar = VideoControlBar(
            rightFrame,
            "Side View",
            sideDimensions,
            lambda params: callbacks.updateParameters(View.SIDE, params),
            lambda topLeft, bottomRight: callbacks.cropRegion(View.SIDE, topLeft, bottomRight),
            lambda: callbacks.incrementFrame(View.SIDE),
            lambda: callbacks.startTracking(View.SIDE)
        )
        self._sideControlBar.pack(side=tk.TOP, fill=tk.X)

        self._masterControlBar = MasterControlBar(
            rightFrame,
            callbacks.makePrediction,
            callbacks.linkVideos,
            callbacks.setStumpPosition,
            sideDimensions
        )
        self._masterControlBar.pack(side=tk.TOP)
    
    def render(self, frontRender: Render, sideRender: Render) -> None:
        """
        Renders the given frames in the GUI.
        parameters:
            frontRender: The render data for the front view.
            sideRender: The render data for the side view.
        """
        self._frontView.updateFrame(
            frontRender.frame,
            frontRender.circles,
            frontRender.cropRegion,
            frontRender.verticalLines,
            frontRender.horizontalLines
        )
        self._sideView.updateFrame(
            sideRender.frame,
            sideRender.circles,
            sideRender.cropRegion,
            sideRender.verticalLines,
            sideRender.horizontalLines
        )