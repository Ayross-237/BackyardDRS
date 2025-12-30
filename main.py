from Model import *
from View import *
from Controller import *
from tkinter import filedialog
from tkinter import messagebox

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


def getInitialInformation() -> tuple[str, str, tuple[int]]:
    """
    Creates a Tkinter window to get the initial information from the user: front video path, side video path, and ball colour.
    """
    root = tk.Tk()
    root.title("Backyard DRS")

    front = FileChooser(root, "Front Video Path:")
    front.pack(side=tk.TOP, padx=10, pady=10, expand=True)
    side = FileChooser(root, "Side Video Path:")
    side.pack(side=tk.TOP, padx=10, pady=10, expand=True)

    ballColourSlider = BallColourSlider(root, "Select Ball Colour:")
    ballColourSlider.pack(side=tk.TOP, padx=10, pady=10, expand=True)

    output = None
    def onSubmit():
        nonlocal output
        output = parseInformation(
            front.getFilePath(),
            side.getFilePath(),
            ballColourSlider.getColour()
        )
        root.destroy()

    submitButton = tk.Button(root, text="Submit", command=onSubmit)
    submitButton.pack(side=tk.TOP, padx=10, pady=10, expand=True)

    root.mainloop()
    return output

def parseInformation(frontPath: str, sidePath: str, colour: tuple[int]) -> tuple[str, str, tuple[int]]:
    """
    Parses the information from the Tkinter window and returns it.
    Args:
        frontPath (str): The front video path.
        sidePath (str): The side video path.
        colour (tuple[int]): The RGB colour tuple.
    """
    if not frontPath:
        messagebox.showerror("Input Error", "Please provide a valid front video path.")
        return
    
    if not sidePath:
        messagebox.showerror("Input Error", "Please provide a valid side video path.")
        return

    if sidePath == frontPath:
        messagebox.showerror("Input Error", "Front and side video paths cannot be the same.")
        return
    
    return (frontPath, sidePath, colour)

if __name__ == "__main__":
    frontPath, sidePath, ballColour = getInitialInformation()

    frontVideo = Video(frontPath, ballColour)
    sideVideo = Video(sidePath, ballColour)
    if not (frontVideo.incrementFrame() and sideVideo.incrementFrame()):
            messagebox.showerror("Could not read", "Could not read from video files.")
            quit()
    
    root = tk.Tk()
    controller = Controller(root, frontVideo, sideVideo)
    root.mainloop()

