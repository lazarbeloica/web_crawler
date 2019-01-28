from kMeansApp.transcode import run
from kMeansApp.plotter import plott
import sys

def main():
    if len(sys.argv) < 3:
        print("Not enought data!")
    coordinates = []
    for i in range (2, len(sys.argv)):
        coordinates.append(sys.argv[i])
    print(coordinates)
    K = int(sys.argv[1])
    if run(coordinates, K):
        print("plotting...")
        plott()

if __name__ == "__main__": main()
