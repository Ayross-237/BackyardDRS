from Model import *
from View import *
from Controller import *
from tkinter import messagebox

def getInitialInformation() -> tuple[str, str, tuple[int]]:
    """
    Creates a Tkinter window to get the initial information from the user: front video path, side video path, and ball colour.

    Returns:
        A tuple representing the front video path, side video path and RGB ball colour in that order.
    """
    root = tk.Tk()
    root.title("Backyard DRS")

    front = FileChooser(root, "Front Video Path")
    front.pack(side=tk.TOP, padx=5, pady=5, expand=tk.TRUE, fill=tk.X)
    side = FileChooser(root, "Side Video Path")
    side.pack(side=tk.TOP, padx=5, pady=5, expand=tk.TRUE, fill=tk.X)

    ballColourSlider = BallColourSlider(root, "Select Ball Colour")
    ballColourSlider.pack(side=tk.TOP, padx=5, pady=5, expand=tk.TRUE)

    output = None
    def onSubmit():
        nonlocal output
        output = validateInformation(
            front.getFilePath(),
            side.getFilePath(),
            ballColourSlider.getColour()
        )
        if output is not None:
            root.destroy()

    submitButton = tk.Button(root, text="Launch", command=onSubmit)
    submitButton.pack(side=tk.TOP, padx=5, pady=5, expand=tk.TRUE)

    root.mainloop()
    return output


def validateInformation(frontPath: str, sidePath: str, colour: tuple[int]) -> tuple[str, str, tuple[int]]:
    """
    Parses the information from the Tkinter window and returns it.
    Args:
        frontPath (str): The front video path.
        sidePath (str): The side video path.
        colour (tuple[int]): The RGB colour tuple.
    
    Returns:
        None if the data is invalid. Otherwise the data exactly as stored in the UI elements.
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


def main() -> None:
    """
    Runs the main execution of the program.
    """
    parameters = getInitialInformation()

    # User quits the window
    if parameters is None:
        quit()

    frontPath, sidePath, ballColour = parameters
    frontVideo = Video(frontPath, ballColour)
    sideVideo = Video(sidePath, ballColour)

    # Ensure video can be read from the files before booting the program
    if not (frontVideo.incrementFrame() and sideVideo.incrementFrame()):
            messagebox.showerror("Read Error", "Could not read from video files.")
            quit()
    
    # Run the program and display any unexpected errors.
    try:
        root = tk.Tk()
        Controller(root, frontVideo, sideVideo)
        root.mainloop()
    except Exception as e:
        root.destroy()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()