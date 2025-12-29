from Model import *
from View import *
from Controller import *
from tkinter import filedialog
from tkinter import messagebox

def browse_file(entry: tk.Entry) -> None:
    """
    Opens a file dialog to select a file and updates the given entry with the selected file path.
    """
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def filePathEntry(root: tk.Tk, label_text: str) -> tk.Entry:
    """
    Creates a file path entry with a label and a browse button.
    """
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, padx=5, pady=5, expand=True)

    label = tk.Label(frame, text=label_text)
    label.pack(side=tk.TOP, pady=5, expand=True, fill=tk.X)

    entry = tk.Entry(frame, width=50)
    entry.pack(side=tk.LEFT, padx=5, pady=5)

    browse_button = tk.Button(frame, text="Browse", command=lambda: browse_file(entry))
    browse_button.pack(side=tk.LEFT, padx=5, pady=5)
    return entry

def colourSlider(root: tk.Tk, label: str) -> tk.Scale:
    """
    Creates a colour slider for selecting RGB values.
    """
    return tk.Scale(root, from_=0, to=255, resolution=1, orient=tk.VERTICAL, label=label, length=75)
    
def ballColourSlider(root: tk.Tk, label: str) -> tk.Scale:
    """
    Creates a set of three colour sliders for selecting the RGB values of the ball colour.
    """
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, padx=10, pady=5, expand=True)

    sliderLabel = tk.Label(frame, text=label)
    sliderLabel.pack(side=tk.TOP, padx=10, pady=5, expand=True)

    red = colourSlider(frame, "Red")
    red.pack(side=tk.LEFT, padx=10, pady=10)
    green = colourSlider(frame, "Green")
    green.pack(side=tk.LEFT, padx=10, pady=10)
    blue = colourSlider(frame, "Blue")
    blue.pack(side=tk.LEFT, padx=10, pady=10)

    return (red, green, blue)

def getInitialInformation() -> tuple[str, str, tuple[int]]:
    """
    Creates a Tkinter window to get the initial information from the user: front video path, side video path, and ball colour.
    """
    root = tk.Tk()
    root.title("Backyard DRS")

    front = filePathEntry(root, "Front Video Path:")
    side = filePathEntry(root, "Side Video Path:")

    r, g, b = ballColourSlider(root, "Select Ball Colour:")

    output = None
    def onSubmit():
        nonlocal output
        output = parseInformation(root, front, side, r, g, b)

    submitButton = tk.Button(root, text="Submit", command=onSubmit)
    submitButton.pack(side=tk.TOP, padx=10, pady=10, expand=True)

    root.mainloop()
    return output

def parseInformation(root: tk.Tk, front: tk.Entry, side: tk.Entry, r: tk.Scale, g: tk.Scale, b: tk.Scale) -> tuple[str, str, tuple[int]]:
    """
    Parses the information from the Tkinter window and returns it.
    Args:
        root (tk.Tk): The Tkinter root window.
        front (tk.Entry): The entry for the front video path.
        side (tk.Entry): The entry for the side video path.
        r (tk.Scale): The red colour slider.
        g (tk.Scale): The green colour slider.
        b (tk.Scale): The blue colour slider.
    """
    frontPath = front.get()
    if not frontPath:
        messagebox.showerror("Input Error", "Please provide a valid front video path.")
        return
    
    sidePath = side.get()
    if not sidePath:
        messagebox.showerror("Input Error", "Please provide a valid side video path.")
        return

    if sidePath == frontPath:
        messagebox.showerror("Input Error", "Front and side video paths cannot be the same.")
        return
    
    ballColour = (r.get(), g.get(), b.get())
    root.destroy()
    return (frontPath, sidePath, ballColour)

if __name__ == "__main__":
    vid = cv.VideoCapture("asdfasdfad")
    vid.read()
    frontPath, sidePath, ballColour = getInitialInformation()

    frontVideo = Video(frontPath, ballColour)
    sideVideo = Video(sidePath, ballColour)
    if not (frontVideo.incrementFrame() and sideVideo.incrementFrame()):
            messagebox.showerror("Could not read", "Could not read from video files.")
            quit()
    
    root = tk.Tk()
    controller = Controller(root, frontVideo, sideVideo)
    root.mainloop()

