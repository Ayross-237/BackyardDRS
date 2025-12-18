import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Create root window
root = tk.Tk()
root.title("Matplotlib in Tkinter")

# Create a matplotlib figure
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 5, 2, 8])
ax.set_title("Sample Plot")

# Embed the figure in Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

root.mainloop()