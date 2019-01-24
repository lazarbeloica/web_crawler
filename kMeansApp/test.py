import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

def get_num_of_coor_from_csv(name):
    with open('myfile.txt') as f:
        first_line = f.readline()
    return first_line.count(',') # num of separators is num of coordinates

def get_data_from_csv(name):
    x = [[],[],[]]
    c = []

    with open('frames/point1.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            print(len(row))
            for i in range(0, (len(row) - 1)):
                x[i].append(int(row[i]))

            c.append(int(row[len(row) - 1]))

        return (x, c)

colormap = np.array(['r', 'g', 'b'])

fig, ax = plt.subplots()
fig.set_tight_layout(True)

px, c = get_data_from_csv("frames/point1.csv")
cx = get_data_from_csv("frames/center1.csv")[0]

print (cx[0])
print (cx[1])
ax.scatter(px[0], px[1], s=50, c=colormap[c])
ax.scatter(cx[0], cx[1], s=50, c='y')

def update(i):
    print(i)

    px, c = get_data_from_csv("frames/point{}.csv".format(i))
    cx = get_data_from_csv("frames/point{}.csv".format(i))[0]

    ax.scatter(px[0], px[1], s=50, c=colormap[c])
    ax.scatter(cx[0], cx[1], s=50, c=colormap['y'])

    return ax,


# FuncAnimation will call the 'update' function for each frame; here
# animating over 10 frames, with an interval of 200ms between frames.
anim = FuncAnimation(fig, update, frames=np.arange(1, 10), interval=200)
if len(sys.argv) > 1 and sys.argv[1] == 'save':
    anim.save('line.gif', dpi=80, writer='imagemagick')
else:
    # plt.show() will just loop the animation forever.
    plt.show()
