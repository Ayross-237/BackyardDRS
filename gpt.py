import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# -----------------------------
# Ball detection (simple)
# -----------------------------
def detect_ball(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 1.5)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=100,
        param2=20,
        minRadius=5,
        maxRadius=20,
    )

    if circles is not None:
        x, y, r = np.uint16(circles[0][0])
        return x, y, r
    return None

# -----------------------------
# Main App
# -----------------------------
class CricketBallTrackingApp:
    def __init__(self, root):
        self.root = root
        root.title("Cricket Ball Tracking (Broadcast Style)")

        self.front_cap = None
        self.side_cap = None

        self.front_pts = []
        self.side_pts = []

        self.stump_x = None

        self.build_ui()
        self.update()

    def build_ui(self):
        self.front_label = tk.Label(self.root)
        self.front_label.grid(row=0, column=0)

        self.side_label = tk.Label(self.root)
        self.side_label.grid(row=0, column=1)
        self.side_label.bind("<Button-1>", self.set_stumps)

        controls = tk.Frame(self.root)
        controls.grid(row=1, column=0, columnspan=2)

        tk.Button(controls, text="Load Front View", command=self.load_front).pack(side="left")
        tk.Button(controls, text="Load Side View", command=self.load_side).pack(side="left")

        self.output = tk.Label(self.root, text="Prediction: —")
        self.output.grid(row=2, column=0, columnspan=2)

    # -----------------------------
    # Load videos
    # -----------------------------
    def load_front(self):
        path = filedialog.askopenfilename()
        if path:
            self.front_cap = cv2.VideoCapture(path)

    def load_side(self):
        path = filedialog.askopenfilename()
        if path:
            self.side_cap = cv2.VideoCapture(path)

    # -----------------------------
    # User defines stumps
    # -----------------------------
    def set_stumps(self, event):
        self.stump_x = event.x
        self.compute_prediction()

    # -----------------------------
    # Core prediction logic
    # -----------------------------
    def compute_prediction(self):
        if len(self.side_pts) < 5 or len(self.front_pts) < 5 or self.stump_x is None:
            return

        # SIDE VIEW: Parabolic fit (height vs distance)
        side_x = np.array([p[0] for p in self.side_pts])
        side_y = np.array([p[1] for p in self.side_pts])

        coeffs = np.polyfit(side_x, side_y, 2)
        predicted_height = np.polyval(coeffs, self.stump_x)

        # FRONT VIEW: Linear fit (ball line)
        front_x = np.array([p[0] for p in self.front_pts])
        front_y = np.array([p[1] for p in self.front_pts])
        line_coeffs = np.polyfit(front_x, front_y, 1)

        self.output.config(
            text=f"Predicted height at stumps (px): {predicted_height:.1f}"
        )

        self.draw_front_prediction(line_coeffs)

    # -----------------------------
    # Drawing
    # -----------------------------
    def draw_front_prediction(self, coeffs):
        if not self.front_cap:
            return

        self.front_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = self.front_cap.read()
        if not ret:
            return

        h, w, _ = frame.shape
        x_vals = np.array([0, w])
        y_vals = coeffs[0] * x_vals + coeffs[1]

        cv2.line(
            frame,
            (int(x_vals[0]), int(y_vals[0])),
            (int(x_vals[1]), int(y_vals[1])),
            (0, 0, 255),
            2,
        )

        self.show_frame(frame, self.front_label)

    # -----------------------------
    # Main loop
    # -----------------------------
    def update(self):
        # Front view
        if self.front_cap and self.front_cap.isOpened():
            ret, frame = self.front_cap.read()
            if ret:
                ball = detect_ball(frame)
                if ball:
                    x, y, r = ball
                    self.front_pts.append((x, y))
                    cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                self.show_frame(frame, self.front_label)

        # Side view
        if self.side_cap and self.side_cap.isOpened():
            ret, frame = self.side_cap.read()
            if ret:
                ball = detect_ball(frame)
                if ball:
                    x, y, r = ball
                    self.side_pts.append((x, y))
                    cv2.circle(frame, (x, y), r, (255, 0, 0), 2)

                if self.stump_x:
                    cv2.line(frame, (self.stump_x, 0), (self.stump_x, frame.shape[0]), (0, 0, 255), 2)

                self.show_frame(frame, self.side_label)

        self.root.after(30, self.update)

    def show_frame(self, frame, label):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(rgb))
        label.imgtk = img
        label.config(image=img)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CricketBallTrackingApp(root)
    root.mainloop()
