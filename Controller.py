import cv2 as cv
import tkinter as tk
from tkinter import messagebox
from library import *
from PIL import Image, ImageTk

class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view

    