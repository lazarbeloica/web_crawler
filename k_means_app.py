from kMeansApp.transcode import run, get_help
from kMeansApp.plotter import plot
import argparse, sys


def usage():
    usage = "Expected parameters are: K <input_data> [ <input_data>]\n" + get_help()
    return usage

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('K', help='Number of clusters to make')
    parser.add_argument('coordinates', help='A comma separated list of input data to use.\n{}'.format(get_help()))
    parser.add_argument('--save', help='Flag to save the algorithm visualisation as gif', action="store_true")
    parser.add_argument('--plot_in_3d', help='Plot in 3D', action="store_true")

    args = parser.parse_args()

    coordinates = args.coordinates.split(',')
    K = int(args.K)

    if run(coordinates, K):
        print("plotting...")
        if args.save:
            plot("save", args.plot_in_3d)
        else:
            plot("gif", args.plot_in_3d)

if __name__ == "__main__": main()
