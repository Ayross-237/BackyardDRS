from Model import *
from View import *
from Controller import *
from tkinter import messagebox

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
    parameters = None
    
    while parameters is None:
        parameters = getInitialInformation()

    frontPath, sidePath, ballColour = parameters
    frontVideo = Video(frontPath, ballColour)
    sideVideo = Video(sidePath, ballColour)
    if not (frontVideo.incrementFrame() and sideVideo.incrementFrame()):
            messagebox.showerror("Read Error", "Could not read from video files.")
            quit()
    
    try:
        root = tk.Tk()
        controller = Controller(root, frontVideo, sideVideo)
        root.mainloop()
    except Exception as e:
        root.destroy()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")