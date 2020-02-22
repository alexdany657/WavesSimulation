import consts
import json

import sys

import matplotlib.pyplot as plt
from matplotlib import animation

#job = "save" # save to ps
job = "draw" # draw online

precalc = []

fig = None
line1 = None
line2 = None
text = None
func = []
ogib = []

def load():
    global precalc, func, ogib
    try:
        dataFile = open(consts.constructFilename(), 'r')
        precalc = json.load(dataFile)
        dataFile.close()
        for a in precalc:
            func.append([list(map(lambda x: x, a[0])), list(map(lambda x: x[0], a[1]))])
            ogib.append([list(map(lambda x: x, a[0])), list(map(lambda x: (x[0]**2 + x[1]**2)**0.5, a[1]))])
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
    global fig, line1, line2, text, func, ogib

    def init():
        return line1, line2, text

    def animate(i):
        line1.set_data(*func[i])
        line2.set_data(*ogib[i])
        text.set_text(str(consts.t[i]))
        #plt.show(block=False)
        #plt.savefig("result/" + consts.constructFilename() + '/' + str(i) + ".ps", format="ps")
        return line1, line2, text

    return animation.FuncAnimation(fig, animate, init_func=init, frames=fr, interval=inter, repeat=True, save_count=fr)

def main() -> int:
    global fig, line1, line2, text
    load()
    fig = plt.figure()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    axes = plt.axes()
    line1, = axes.plot([], [], "g-", lw=1)
    line2, = axes.plot([], [], "b-", lw=1)
    text = axes.text(consts.xRange[0]+abs(consts.xRange[0])*0.1, consts.yRange[1]-.1, "")
    axes.set_xlim(*consts.xRange)
    axes.set_ylim(*consts.yRange)
    if (job == "draw"):
        _ = waveAnimation(consts.frames, consts.interval)
        plt.show()
        return 0
    for i in range(consts.frames):
        text.set_text(chr(8722)*(consts.t[i]<0)+str(abs(consts.t[i])))
        line1.set_data(*precalc[i])
        plt.show(block=False)
        plt.savefig("result/" + consts.constructFilename() + '/' + str(i).zfill(4) + ".ps", format="eps", orientation="portrait", papertype="a4")
        print(i)
    #plt.show()
    return 0

if __name__ == "__main__":
    main()
