import tkinter as tk
from tkinter import messagebox
from library import *
from Model import *
from View import *

class Controller:
    def __init__(self, root: tk.Tk, frontVideo: Video, sideVideo: Video) -> None:
        """
        Initializes the Controller with the given side and front video sources and sets up the Model and View.
        Args:
            sideVideo (Video): The video source for the side camera.
            frontVideo (Video): The video source for the front camera.
        """        
        self._frontDimensions = frontVideo.getDimensions()
        self._sideDimensions = sideVideo.getDimensions()
        self._model = Model(frontVideo, sideVideo)

        callbacks = Callbacks(
            incrementFrame=self.incrementFrame,
            updateParameters=self.updateParameters,
            cropRegion=self.cropRegion,
            startTracking=self.startTracking,
            setStumpPosition=self.setStumpPosition,
            makePrediction=self.makePrediction,
            linkVideos=self.linkVideos
        )
        self._view = VIEW(root, frontVideo.getDimensions(), sideVideo.getDimensions(), callbacks)
        self.update_view()
    
    def update_view(self) -> None:
        """
        Updates the View with the latest rendered frames from the Model.
        """
        renders = self._model.render()
        frontRender = renders[View.FRONT]
        sideRender = renders[View.SIDE]
        self._view.render(frontRender, sideRender)
    
    def incrementFrame(self, view: View) -> None:
        """
        Increments the frame for the specified view (FRONT or SIDE).
        Args:
            view (View): The view to increment the frame for.
        """
        if not self._model.incrementFrame(view):
            messagebox.showinfo("End of Video", f"No more frames in {view.name} video.")
        else:
            self.update_view()
    
    def updateParameters(self, view: View, parameters: Parameters) -> None:
        """
        Updates the tracking parameters for the specified view (FRONT or SIDE).
        Args:
            view (View): The view to update the parameters for.
            parameters (Parameters): The new tracking parameters.
        """
        self._model.updateParameters(view, parameters)
        self.update_view()
    
    def cropRegion(self, view: View, topleft: tuple[int], bottomright: tuple[int]) -> None:
        """
        Updates the crop region for the specified view (FRONT or SIDE).
        Args:
            view (View): The view to update the crop region for.
            cropRegion (tuple[tuple[int]]): The new crop region as ((x1, y1), (x2, y2)).
        """
        self._model.cropRegion(view, topleft, bottomright)
        self.update_view()
    
    def setStumpPosition(self, position: int) -> None:
        """
        Sets the stump position in the side video.
        Args:
            position (int): The x-coordinate of the stump position.
        """
        if position < 0 or position > self._sideDimensions[0]:
            messagebox.showerror("Invalid Position", "Stump position must be within the width of the side video.")
        else:
            self._model.setStumpPosition(position)
            self.update_view()
    
    def startTracking(self, view: View) -> None:
        """
        Starts ball tracking for the specified view (FRONT or SIDE).
        Args:
            view (View): The view to start tracking for.
        """
        if self._model.startTracking(view):
            messagebox.showinfo("Tracking Started", f"Started tracking in {view.name} video.")
        else:
            messagebox.showerror("Tracking Error", f"Already started tracking or no frames available.")
    
    def makePrediction(self) -> None:
        """
        Makes a prediction based on the tracked data and updates the View to display the results.
        """
        output = None
        # Attempt to make prediction and handle potential errors
        try:
            output = self._model.makePrediction()
        except ValueError as e:
            messagebox.showerror("Could not make prediction: ", str(e))
            return
        
        # Update the front view to draw the predicted line of the ball upon impact
        renders = self._model.render()
        frontRender = renders[View.FRONT]
        frontRender.circles=[]
        frontRender.cropRegion=None
        frontRender.verticalLines=[output[0]]

        # Update the side view to draw the predicted height of the ball upon impact
        sideRender = renders[View.SIDE]
        sideRender.circles=[]
        sideRender.cropRegion=None
        sideRender.verticalLines=[]
        sideRender.horizontalLines=[output[1]]
        
        self._view.render(frontRender, sideRender)

    def linkVideos(self) -> None:
        """
        Links the side and front videos for synchronized playback.
        """
        self._model.linkVideos()