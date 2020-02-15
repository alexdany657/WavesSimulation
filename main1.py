import math
import sys

from scipy.integrate import quad

from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

DEBUG = False

# functions

def ft(f_w, w, x, t):
    _f = lambda k: complex(f_w(k) * math.e ** ((0+1j)*(w(k)*t-k*x))).real
    N = 11
    M = 500
    summ = (0+0j)
    for i in range(int(-(k_0+.5)*M),int((-k_0+.5)*M+1)):
        k = i / M
        summ += f_w(k) / M * math.e ** ((0+1j)*(w(k)*t-k*x))
    return summ
    #return quad(_f, -2, 0)[0]

# -----------------------------------------------------
# consts

A = 10
B = 1
k_0 = 1
w_0 = 1

w = lambda k: w_0 * abs(k) ** 0.5
print(w(-1))
f_w = lambda k: A/2/math.pi**0.5*math.e**(-A**2*(k+k_0)**2/4)
f = lambda x,t: ft(f_w, w, x, .1*t)
#f = lambda x,t: B*math.e**(-x**2/A**2)*math.e**(-(0+1j)*k_0*x)

xLim = 50
xStep = 1e-1

x = np.arange(-xLim,xLim+xStep,xStep)

xRange, yRange = [-xLim, xLim], [-1.1, 1.1]

frames = 500
interval = 50
t = np.arange(0,frames,1)

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
        _y.append(f(__x, t).real)
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
            if (DEBUG):
                print("Started precalc")
            if precalc != []:
                if (DEBUG):
                    print("Using cached data!")
                return self.line, self.text
            
            #tmp = [None for _ in range(fr)]
            #for i in range(fr):
            #    tmp[i] = plot(t[i])
            #    print(i)

            with Pool(4) as p:
                tmp = p.map(plot, t)

            precalc = tmp

            if (DEBUG):
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
