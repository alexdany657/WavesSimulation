import consts
from multiprocessing import Pool
import json
import time
import math
import cmath

def ft(f_w, w, x, t):
    summ = 0
    for i in range(int(-(consts.k_0+abs(consts.k_0))*consts.M),int((-consts.k_0+abs(consts.k_0))*consts.M+1)):
        k = i / consts.M
        summ += f_w(k) / consts.M * cmath.exp((0+1j)*(w(k)*t-k*x))
    return [summ.real, summ.imag]

w = lambda k: consts.w_0 * abs(k) ** consts.w_p
f_w = lambda k: consts.B * consts.A/2/math.pi**0.5*math.exp(-consts.A**2*(k+consts.k_0)**2/4)
f = lambda x,t: ft(f_w, w, x, t)

def plot(t):
    _y = []
    _x = []
    for __x in consts.x:
        _x.append(__x)
        _y.append(f(__x, t))
    print(t)
    return (_x, _y)

def precalc() -> int:
    zero = time.time()
    with Pool(4) as p:
        precalc = p.map(plot, consts.t)
    #
    dataFile = open(consts.constructFilename(), 'w')
    json.dump(precalc, dataFile)
    dataFile.close()
    print(time.time() - zero)
    return 0

def main() -> int:
    precalc()
    return 0

if __name__ == "__main__":
    main()
