from Model import *
from View import *
from library import *

video = Video("Tests/5/ball.mp4", (255, 255, 255))
video.incrementFrame()
print(video.getDimensions())
print(video.getFPS())

side = Video("Tests/5/side.mp4", (255, 255, 255))
side.incrementFrame()
print(side.getDimensions())
print(side.getFPS())

model = Model(video, side)

root = tk.Tk()
root.title("Backyard DRS")
video.incrementFrame()
view = VideoView(root, 540, 960)
view.getLabel().pack(side=tk.LEFT)
newFrame = video.getCurrentFrame()

rightFrame = tk.Frame(root)
rightFrame.pack(side=tk.LEFT, fill=tk.BOTH)
sideView = VideoView(rightFrame, 960, 540)
sideView.getLabel().pack(side=tk.TOP)


def updateView():
    renderings = model.render()
    frontRender = renderings[View.FRONT]
    sideRender = renderings[View.SIDE]
    view.updateFrame(frontRender.frame, frontRender.circles, frontRender.cropRegion, frontRender.verticalLines)
    sideView.updateFrame(sideRender.frame, sideRender.circles, sideRender.cropRegion, sideRender.verticalLines)

def incrementAndUpdate(view: View):
    model.incrementFrame(view)
    updateView()

def updateParams(view: VideoView, parameters):
    model.updateParameters(view, parameters)
    updateView()

def updateCropRegion(view: View, start, end):
    model.cropRegion(view, start, end)
    updateView()

def updateStumpPosition(x):
    model.setStumpPosition(x)
    updateView()

controlBar = VideoControlBar(
    rightFrame, "Front Angle", video.getDimensions(),
    lambda params: updateParams(View.FRONT, params),
    lambda start, end: updateCropRegion(View.FRONT, start, end),
    lambda: incrementAndUpdate(View.FRONT),
    lambda: model.markFirstFrame(View.FRONT)
)
controlBar.getFrame().pack(side=tk.TOP, fill=tk.X)
controlBar2 = VideoControlBar(
    rightFrame, "Side Angle", side.getDimensions(),
    lambda params: updateParams(View.SIDE, params),
    lambda start, end: updateCropRegion(View.SIDE, start, end),
    lambda: incrementAndUpdate(View.SIDE),
    lambda: model.markFirstFrame(View.SIDE)
)
controlBar2.getFrame().pack(side=tk.TOP, fill=tk.X)

master = MasterControlBar(rightFrame, model.makePrediction, model.linkVideos, updateStumpPosition, side.getDimensions())
master.getFrame().pack(side=tk.TOP, fill=tk.X)

root.mainloop() 