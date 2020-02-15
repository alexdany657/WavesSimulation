import consts
import json

import sys

import matplotlib.pyplot as plt
from matplotlib import animation

precalc = []

def load():
    global precalc
    try:
        dataFile = open(consts.constructFilename(), 'r')
        precalc = json.load(dataFile)
        dataFile.close()
    except FileNotFoundError:
        print("Failed to find data")
        sys.exit(1)

def waveAnimation(fr=100, inter=50):
    print(len(precalc))
    fig = plt.figure()
    axes = plt.axes()
    line, = axes.plot([], [], "g-", lw=2)
    text = axes.text(consts.xRange[0]+1, consts.yRange[1]-.1, "")
    axes.set_xlim(*consts.xRange)
    axes.set_ylim(*consts.yRange)

    def init():
        return line, text

    def animate(i):
        line.set_data(*precalc[i])
        text.set_text(str(consts.t[i]))
        return line, text

    return animation.FuncAnimation(fig, animate, init_func=init, frames=fr, interval=inter, repeat=True, save_count=fr)

def main() -> int:
    load()
    _ = waveAnimation(consts.frames, consts.interval)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    return 0

if __name__ == "__main__":
    main()
