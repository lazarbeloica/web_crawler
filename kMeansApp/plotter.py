import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import matplotlib
import os

colormap = np.array(['grey','red','green','blue','yellow','brown','orange','purple','pink','cyan','olive'])
fig, ax = plt.subplots()

def get_data_from_csv(name):
    x = []
    columns = 0
    with open(name, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        tmp_reader = csv.reader(csvfile, delimiter=',')

        columns = len(next(tmp_reader))
        del tmp_reader

    with open(name, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        for n in range(columns):
            x.append([])

        for row in spamreader:
            for i in range(len(row)):
                x[i].append(int(float(row[i])))
    return x, columns

def draw_graph(data, columns, centers):

    ax.cla()
    if (columns == 3):
        ax.scatter(data[0], data[1], s=50, c=colormap[data[columns - 1]])
        ax.scatter(centers[0], centers[1], s=50, c='black')
    elif (columns > 3):
        ax.scatter(data[0], data[1], data[2], s=50, c=colormap[data[columns - 1]])
        ax.scatter(centers[0], centers[1], centers[2], s=50, c='black')
    else:
        raise RuntimeError("U kom svetu ti zivis!?")

    return ax

def update(i):
    px, columns = get_data_from_csv("kMeansApp/frames/point{}.csv".format(int(i)))
    cx = get_data_from_csv("kMeansApp/frames/center{}.csv".format(int(i)))[0]

    ax = draw_graph(px, columns, cx)
    label = 'Iteration: {}'.format(int(i))
    ax.set_xlabel(label)
    return ax

def plott():
    num_frames = sum([len(files) for r, d, files in os.walk("kMeansApp/frames/")]) / 2
    fig.set_tight_layout(True)

    px, columns = get_data_from_csv("kMeansApp/frames/point0.csv")

    cx = get_data_from_csv("kMeansApp/frames/center0.csv")[0]

    draw_graph(px, columns, cx)

    anim = FuncAnimation(fig, update, frames=np.arange(1, num_frames), interval=700)
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('line.gif', dpi=80, writer='imagemagick')
    else:
        plt.show()


if __name__ == "__main__": plott()
