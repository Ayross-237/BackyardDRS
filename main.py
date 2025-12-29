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
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, padx=10, pady=5, expand=True)

    label = tk.Label(frame, text=label_text)
    label.pack(side=tk.TOP, padx=10, pady=5, expand=True)

    entry = tk.Entry(frame, width=50)
    entry.pack(side=tk.LEFT, padx=5, pady=5)

    browse_button = tk.Button(frame, text="Browse", command=lambda: browse_file(entry))
    browse_button.pack(side=tk.LEFT, padx=5, pady=5)
    return entry

def colourSlider(root: tk.Tk, label: str) -> tk.Scale:
    return tk.Scale(root, from_=0, to=255, resolution=1, orient=tk.VERTICAL, label=label, length=75)
    
def ballColourSlider(root: tk.Tk, label: str) -> tk.Scale:
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
    root = tk.Tk()
    root.title("Backyard DRS")

    front = filePathEntry(root, "Front Video Path:")
    side = filePathEntry(root, "Side Video Path:")

    r, g, b = ballColourSlider(root, "Select Ball Colour:")

    submitButton = tk.Button(root, text="Submit", command=lambda: retrieveInitialInformation(root, front, side, r, g, b))
    submitButton.pack(side=tk.TOP, padx=10, pady=10, expand=True)
    root.mainloop()

def retrieveInitialInformation(root: tk.Tk, front: tk.Entry, side: tk.Entry, r: tk.Scale, g: tk.Scale, b: tk.Scale) -> tuple[str, str, tuple[int]]:
    frontPath = front.get()
    if not frontPath:
        messagebox.showerror("Input Error", "Please provide a valid front video path.")
        return
    
    sidePath = side.get()
    if not sidePath:
        messagebox.showerror("Input Error", "Please provide a valid side video path.")
        return
    
    ballColour = (r.get(), g.get(), b.get())
    root.destroy()
    return (frontPath, sidePath, ballColour)

if __name__ == "__main__":
    #frontPath, sidePath, ballColour = getInitialInformation()
    print(getInitialInformation())
