import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.animation as animation
import constants as c
import functions as f
import init
from classes import BigBody, probe
from matplotlib.colors import SymLogNorm

# Some Constants
frames = int(c.tspan/c.dt)

# Figure
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(6, 6))
fig.set_facecolor('#303030')
ax.set_facecolor('#303030')

SourceList = c.SourceList
ProbeList  = c.ProbeList

# To record the position of the probes
X = np.zeros((len(ProbeList), frames))
Y = np.zeros((len(ProbeList), frames))
aCor = np.zeros((len(ProbeList), frames, 2))
aCen = np.zeros((len(ProbeList), frames, 2))
aG   = np.zeros((len(ProbeList), frames, 2))

for i in tqdm(range(int(frames))):
    for j, Probe in enumerate(ProbeList):
        Probe.update(c.dt)
        X[j,i] = Probe.x
        Y[j,i] = Probe.y
        aCor[j,i,:] = Probe.acor[:2]
        aCen[j,i,:] = Probe.acen[:2]
        aG[j,i,:] = Probe.ag[:2]

# Lagrange point positions
f.Plot_Static(SourceList, fig, ax)

# Gravi. Field Contour
f.Plot_Contour(SourceList, fig, ax)

# Animations
def update(i):
    lines = []
    dots = []
    arracors = []
    arracens = []
    arrags = []
    for j, Probe in enumerate(ProbeList):
        lines.append(ax.plot(X[j, max(0, i-c.tail):i], Y[j, max(0, i-c.tail):i], color='cyan', linestyle='-', linewidth=1)[0])
        dots.append( ax.plot(X[j,i], Y[j,i], color='cyan', linestyle='-', markersize=5, marker='o')[0])
        arracors.append(ax.arrow(X[j,i], Y[j,i], aCor[j,i,0]*c.resize, aCor[j,i,1]*c.resize, head_width=c.arrowsize, head_length=c.arrowsize, fc='r', ec='r'))
        arracens.append(ax.arrow(X[j,i], Y[j,i], aCen[j,i,0]*c.resize, aCen[j,i,1]*c.resize, head_width=c.arrowsize, head_length=c.arrowsize, fc='y', ec='y'))
        arrags.append(ax.arrow(X[j,i], Y[j,i], aG[j,i,0]*c.resize,   aG[j,i,1]*c.resize,   head_width=c.arrowsize, head_length=c.arrowsize, fc='skyblue', ec='skyblue'))
    return dots + lines + arracors + arracens + arrags

# Set Boxsize, etc.
f.set_plot_dimensions(fig, ax)

ani = animation.FuncAnimation(
    fig=fig,
    func=update,
    frames=np.arange(0, frames, 2),
    interval=1000/int(frames),
    blit=True,
    repeat=False)
#ani.save("movie.mp4", dpi=300, fps=20)

if c.SAVE_VIDEO:
    for i, frame in enumerate(tqdm(np.arange(0, frames, 20))):
        f.save_frame(i, frame, SourceList, ProbeList, X, Y, aCor, aCen, aG, fig, ax)
else:
    plt.show()
