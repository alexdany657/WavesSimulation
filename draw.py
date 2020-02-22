import consts
import json

import sys

import matplotlib.pyplot as plt
from matplotlib import animation

#job = "save" # save to ps
job = "draw" # draw online

precalc = []

fig = None
line = None
text = None

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
    #fig = plt.figure()
    #axes = plt.axes()
    #line, = axes.plot([], [], "g-", lw=2)
    #text = axes.text(consts.xRange[0]+1, consts.yRange[1]-.1, "")
    #axes.set_xlim(*consts.xRange)
    #axes.set_ylim(*consts.yRange)
    global fig, line, text

    def init():
        return line, text

    def animate(i):
        line.set_data(*precalc[i])
        text.set_text(str(consts.t[i]))
        #plt.show(block=False)
        #plt.savefig("result/" + consts.constructFilename() + '/' + str(i) + ".ps", format="ps")
        return line, text

    return animation.FuncAnimation(fig, animate, init_func=init, frames=fr, interval=inter, repeat=True, save_count=fr)

def main() -> int:
    global fig, line, text
    load()
    fig = plt.figure()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    axes = plt.axes()
    line, = axes.plot([], [], "g-", lw=1)
    text = axes.text(consts.xRange[0]+abs(consts.xRange[0])*0.1, consts.yRange[1]-.1, "")
    axes.set_xlim(*consts.xRange)
    axes.set_ylim(*consts.yRange)
    if (job == "draw"):
        _ = waveAnimation(consts.frames, consts.interval)
        plt.show()
        return 0
    for i in range(consts.frames):
        text.set_text(chr(8722)*(consts.t[i]<0)+str(abs(consts.t[i])))
        line.set_data(*precalc[i])
        plt.show(block=False)
        plt.savefig("result/" + consts.constructFilename() + '/' + str(i).zfill(4) + ".ps", format="eps", orientation="portrait", papertype="a4")
        print(i)
    #plt.show()
    return 0

if __name__ == "__main__":
    main()
