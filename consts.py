import numpy as np

def constructFilename():
    return "linWave_"+str(A)+'_'+str(B)+'_'+str(k_0)+'_'+str(w_0)+'_'+str(w_p)+'_'+str(xLim)+'_'+str(xStep)+'_'+str(frames)+'_'+str(M)

A = 10 #IMPORTANT
B = 1 #IMPORTANT
k_0 = 1 #IMPORTANT
w_0 = .5 #IMPORTANT
w_p = 0.5 #VERY_IMPORTANT !!!

xLim = 200 #IMPORTANT
xStep = 1e-1 #IMPORTANT

M = 500 #IMPORTANT

xRange, yRange = [-xLim, xLim], [-1.1, 1.1]

x = np.arange(-xLim,xLim+xStep,xStep)

frames = 100 #IMPORTANT
interval = 50
t = np.arange(-frames//2,frames-frames//2,1)

if __name__ == "__main__":
    print(constructFilename())
