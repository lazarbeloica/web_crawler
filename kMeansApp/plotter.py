import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import matplotlib
import os
from mpl_toolkits.mplot3d import Axes3D
from decimal import Decimal

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

        for n in range(0,columns):
            x.append([])

        for row in spamreader:
            for i in range(0, columns):
                x[i].append(int(float(row[i])))

    return x

class PointPlotter():
    colormap = np.array(['red','green','blue','yellow','brown','orange','purple','pink','cyan','olive', 'grey'])

    def __init__(self, points, frames_dir, plt, plot_in_3d = False):
        self.px = points
        self.frames_dir = frames_dir
        self.columns = len(points)
        self.plt = plt
        self.plot_in_3d = plot_in_3d
        if plot_in_3d:
            self.fig = self.plt.figure()
            self.ax =  Axes3D(self.fig)
        else:
            self.fig, self.ax = self.plt.subplots()

        self.default_colour = self.create_default_colour_scheme(len(self.px[0]))


    def create_default_colour_scheme(self, n):
        c = []
        for i in range(0, n):
            c.append(len(self.colormap) - 1)
        return c

    def draw_graph(self, data, colours, centers):
        columns = len(data)
        if (columns == 2):
            self.ax.scatter(data[0], data[1], s=10, c=self.colormap[colours])
            self.ax.scatter(centers[0], centers[1], s=30, c='black')
        elif (columns == 3):
            if self.plot_in_3d:
                self.ax.scatter(data[0], data[1], zs=data[2], zdir='z', s=10, c=self.colormap[colours])
                self.ax.scatter(centers[0], centers[1], zs=centers[2], zdir='z', s=50, c='black')
            else:
                raise RuntimeError("You need to print this in 3D. Pass --plot_in_3d option")
        else:
            raise RuntimeError("U kom svetu ti zivis!? {} ose?".format(columns))

        return self.ax

    def update(self, i):
        self.ax.cla()
        colour = get_data_from_csv("{}/pointColour{}.csv".format(self.frames_dir, int(i)))
        cx = get_data_from_csv("{}/center{}.csv".format(self.frames_dir, int(i)))
        self.ax = self.draw_graph(self.px, colour, cx)
        label = 'Iteration: {}'.format(int(i))
        self.ax.set_xlabel(label)
        return self.ax

    def prepare_plot(self):
        num_frames = sum([len(files) for r, d, files in os.walk(self.frames_dir)]) / 2
        self.fig.set_tight_layout(False)
        cx = get_data_from_csv("{}/center0.csv".format(self.frames_dir))

        self.draw_graph(self.px, self.default_colour, cx)

        self.anim = FuncAnimation(self.fig, self.update, frames=np.arange(1, num_frames), interval=700)

    def plot_gif(self):
        self.prepare_plot()
        self.plt.show()

    def save_gif(self):
        self.prepare_plot()
        self.anim.save('graph.gif', dpi=80, writer='imagemagick')

def plot(action, plot_in_3d = False):
    frames_dir = "kMeansApp/frames"
    px = get_data_from_csv("kMeansApp/points.csv")
    point_plotter = PointPlotter(px, frames_dir, plt, plot_in_3d)

    if action == 'save':
        point_plotter.save_gif()
        print("saved")
    else:
        point_plotter.plot_gif()


if __name__ == "__main__": plot()
