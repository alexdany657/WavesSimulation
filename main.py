import math
import sys

from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class App:
    def __init__(self, f, xRange):
        self.fig = plt.figure()
        self.axes = plt.axes()
        self.line, = self.axes.plot([], [], 'g-', lw=2)
        self.text = self.axes.text(-49, 1, "")
        self.t = np.arange(0,100,1)
        self.f = f
        self.xRange = xRange

    def setAxesScale(self, xRange, yRange):
        self.axes.set_xlim(*xRange)
        self.axes.set_ylim(*yRange)

    def _plot(self, t):
        x = []
        y = []
        for _x in self.xRange:
            x.append(_x)
            y.append(self.f(_x, t))
        self.x = x
        self.y = y

    def waveAnimation(self, frames=100, interval=30):
        self.line.set_data([], [])
        self.text.set_text("")
        self.precalc = []

        def _animate(i):
            self._plot(self.t[i])
            #self.line.set_data(self.x, self.y)
            return (self.x, self.y)

        def init():
            print("Started precalc")
            if self.precalc != []:
                print("Using cached data!")
                return self.line

            for i in range(frames):
                self.precalc.append(_animate(i))
                print(i)
            
            #def calc(t):
            #    self._plot(t)
            #    return self.x, self.y

            #with Pool(4) as p:
            #    self.precalc = list(p.map(calc, self.t))

            print("Precalc done")
            #print(*self.precalc)
            return self.line, self.text

        def animate(i):
            #print(self.precalc[i])
            #print(i)
            self.line.set_data(*self.precalc[i])
            self.text.set_text(str(i))
            return self.line, self.text

        return animation.FuncAnimation(self.fig, animate, init_func=init, frames=frames, interval=interval, repeat=True, save_count=frames)

    def show(self):
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show(block=True)

def ft(f_w, w, x, t):
    N = 100
    M = 10
    summ = 0
    for i in range(-N*M,N*M+1):
        k = i / M
        summ += f_w(k) / M * math.e ** ((0+1j)*(w(k)*t-k*x))
    return summ

def main() -> int:
    f_w = lambda k: 1/2/math.pi**0.5*math.e**(-(k)**2/4)
    #f = lambda x, t: math.e**(-((x-.1*t)/4)**2)*math.cos(5*(x-.1*t))
    w = lambda k: (k) ** .5 * 10
    f = lambda x,t: ft(f_w, w, x, .1*t).real
    xLim = 50
    xStep = 1e-1
    app = App(f, np.arange(-xLim,xLim+xStep,xStep))
    app.setAxesScale([-50., 50.], [-1.1, 1.1])
    _ = app.waveAnimation(10,50)
    app.show()
    return 0

if __name__ == "__main__":
    main()
