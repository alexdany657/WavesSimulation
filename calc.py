import consts
from multiprocessing import Pool
import math
import json

def ft(f_w, w, x, t):
    summ = (0+0j)
    for i in range(int(-(consts.k_0+.5)*consts.M),int((-consts.k_0+.5)*consts.M+1)):
        k = i / consts.M
        summ += f_w(k) / consts.M * math.e ** ((0+1j)*(w(k)*t-k*x))
    return summ

w = lambda k: consts.w_0 * abs(k) ** consts.w_p
f_w = lambda k: consts.A/2/math.pi**0.5*math.e**(-consts.A**2*(k+consts.k_0)**2/4)
f = lambda x,t: ft(f_w, w, x, t)

def plot(t):
    _y = []
    _x = []
    for __x in consts.x:
        _x.append(__x)
        _y.append(f(__x, t).real)
    print(t)
    return (_x, _y)

def precalc() -> int:
    with Pool(4) as p:
        precalc = p.map(plot, consts.t)
    #
    dataFile = open(consts.constructFilename(), 'w')
    json.dump(precalc, dataFile)
    dataFile.close()
    return 0

if __name__ == "__main__":
    precalc()
