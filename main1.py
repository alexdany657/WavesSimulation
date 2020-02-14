import math
import sys

from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# functions

def ft(f_w, w, x, t):
    N = 100
    M = 10
    summ = 0
    for i in range(-N*M,N*M+1):
        k = i / M
        summ += f_w(k) / M * math.e ** ((0+1j)*(w(k)*t-k*x))
    return summ

# -----------------------------------------------------
# consts

w = lambda k: (k) ** .5
f_w = lambda k: 1/2/math.pi**0.5*math.e**(-(k)**2/4)
f = lambda x,t: ft(f_w, w, x, .1*t).real

xLim = 50
xStep = 1e-1

x = np.arange(-xLim,xLim+xStep,xStep)

xRange, yRange = [-xLim, xLim], [-1.1, 1.1]

t = np.arange(0,100,1)
frames = 100
interval = 50

# -----------------------------------------------------
# containres

precalc = []

# -----------------------------------------------------
# functions

def plot(t):
    _y = []
    _x = []
    for __x in x:
        _x.append(__x)
        _y.append(f(__x, t))
    print(t)
    return (_x, _y)

# -----------------------------------------------------
# App

class App:
    def __init__(self):
        self.fig = plt.figure()
        self.axes = plt.axes()
        self.line, = self.axes.plot([], [], 'g-', lw=2)
        self.text = self.axes.text(xRange[0]+1, yRange[1]-.1, "")

    def setAxes(self):
        self.axes.set_xlim(*xRange)
        self.axes.set_ylim(*yRange)

    def waveAnimation(self, fr=100, inter=50):
        global precalc

        self.line.set_data([], [])
        self.text.set_text("")
        
        def init():
            global precalc
            print("Started precalc")
            if precalc != []:
                print("Using cached data!")
                return self.line, self.text
            
            #tmp = [None for _ in range(fr)]
            #for i in range(fr):
            #    tmp[i] = plot(t[i])
            #    print(i)

            with Pool(4) as p:
                tmp = p.map(plot, t)

            precalc = tmp

            print("Precalc done")
            return self.line, self.text

        def animate(i):
            self.line.set_data(*precalc[i])
            self.text.set_text(str(t[i]))
            return self.line, self.text

        return animation.FuncAnimation(self.fig, animate, init_func=init, frames=fr, interval=inter, repeat=True, save_count=fr)

    def show(self):
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show(block=True)

def main() -> int:
    app = App()
    app.setAxes()
    _ = app.waveAnimation(frames, interval)
    app.show()
    return 0

if __name__ == "__main__":
    main()
