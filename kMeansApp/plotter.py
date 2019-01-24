import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

colormap = np.array(['r', 'g', 'b'])
x = []
y = []
c = []

with open('frames/point1.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        x.append(int(row[0]))
        y.append(int(row[1]))
        c.append(int(row[2]))

fig, ax = plt.subplots()
fig.set_tight_layout(True)

ax.scatter(x, y, s=50, c=colormap[c])

def update(i):
    print(i)
    x = []
    y = []
    c = []

    with open('frames/point{}.csv'.format(i), 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            x.append(int(row[0]))
            y.append(int(row[1]))
            c.append(int(row[2]))

    ax.scatter(x, y, s=50, c=colormap[c])
    return ax,


anim = FuncAnimation(fig, update, frames=np.arange(1, 10), interval=500)
if len(sys.argv) > 1 and sys.argv[1] == 'save':
    anim.save('line.gif', dpi=80, writer='imagemagick')
else:
    plt.show()
