import matplotlib.pyplot as plt
import numpy as np
import random

from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint

from PriceDemandsSupplies import *

def Lab1():
    prices 	= [3,   4.1,    5.1,    6,  6.8,    7.5,    8.8,    9.4,    10, 11, 11.8,   12.2]
    demands = [116,	90,		74,		63,	53,		43,     38,     32,     29, 25, 24,	    18]
    supplies = [1,	3,		11,		16,	19,		21,		22,		25,		30,	32,	35,		41]
	
    market = Market(prices,demands,supplies)
    market.plotInputData()
    market.plotApproximationsCompare()
    market.plotWithGrant()
    market.printInfo()
    
    plt.show()
    
def Lab2():
    k = [1420,  1510,   1470,   1450,   1500,   1560,   1580,   1405,   1550,   1440]
    l = [2160,  2195,   2020,   2130,   2200,   2220,   2150,   2190,   2235,   2180]
    f = [5105,  5260,   5128,   5115,   5327,   5280,   5324,   5116,   5186,   5142]
    
    surf = Surface(k,l,f)
    surf.approximate()
    surf.printApproximation()
    for i in range(len(k)):
        #print(surf(k[i],l[i]),f[i])
        print(f[i])
    x = np.linspace(min(k),max(k),100)
    y = np.linspace(min(l),max(l),100)
    x, y = np.meshgrid(x, y)
    z = surf(x,y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x,y,z)
    ax.scatter(k,l,f,c='r')
    
    plt.show()

def Lab3():
    matrix = np.array([[0.1,0.2,0.4],[0.3,0.2,0.3],[0.1,0.3,0.2]])
    sum = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])
    temp = matrix
    k=1
    while True:
        curr = np.dot(temp,matrix)
        ok = True
        for i in range(3):
            for j in range(3):
                if abs(curr[i,j]-temp[i,j]) > 0.01:
                    ok = False
        if ok:
            break
        sum+=temp
        k+=1
        temp=curr
    print(sum)
    print(k)
    
def Lab4_1():
    def t_N(N,C=0):
        a = N**15
        b = (N-1)**20
        c = (5*N-2)**35
        return np.log(c/(a*b))/24 + C
        #return -15*np.log(N*(N-1)**(4/3)/(5*N-2)**(7/3))/24 + c
        #return (35*np.log(5*N-2) - 15*np.log(N) - 20*np.log(N-1))/24 + c
        
    def find_c(t,N):
        return t - t_N(N)
        
    def recurent(t0,N0):
        dt = 0.01
        xs = np.arange(t0,10,dt)
        ys = []
        y = N0
        dN = 0
        for x in xs:
            y+=dN
            ys.append(y)
            dN = (-4*y**3 + 5.6*y**2 - 1.6*y)/(1+y)
            dN *= dt
        return xs,np.array(ys)
        
    t0 = 0
    N0 = 2
    
    x,y = recurent(t0,N0)
    
    plt.plot(x,y)
    plt.xlabel("t")
    plt.ylabel("N")
    
    plt.show()
    
def Lab4_2():
    def func(x,c=0):
        return 100*np.exp(0.8*x)/(np.exp(0.8*x) + c)
    
    def find_c(x,y):
        return (100-y)*np.exp(0.8*x)/y
        
    c1 = find_c(0,20)
    c2 = find_c(0,180)
    print(c1,c2)
    print(func(6,c1))
    print(func(6,c2))
    x = np.arange(0,7,0.1)
    y1 = func(x,c1)
    y2 = func(x,c2)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,2)
    
    res_c20 = fig.add_subplot(gs[0,0])
    res_c20.set_title("Start with 20")
    res_c20.plot(x,y1,'b')
    
    res_c180 = fig.add_subplot(gs[0,1])
    res_c180.set_title("Start with 180")
    res_c180.plot(x,y2,'b')
    
    res_together = fig.add_subplot(gs[1,:])
    res_together.set_title("Together")
    res_together.plot(x,y1,'r')
    res_together.plot(x,y2,'g')
    
    plt.show()
    
def Lab4_3():
    tmax = 10
    def test1():
        return 4,2.5,0, 2,1,0
        
    def test2():
        return 4,2.5,0.1, 2,1,0.1
        
    def test3():
        return random.random(),random.random(),random.random(),random.random(),random.random(),random.random()
    
    e1, g11, g12, e2, g21, g22 = test2()
    
    def fN1(n1,n2):
        return (e1 - g11 * n2 - g12 * n1) * n1
    
    def fN2(n1,n2):
        return (-e2 + g21 * n1 - g22 * n2) * n2
        
    def f(Y,t):
        return [fN1(Y[0],Y[1]),fN2(Y[0],Y[1])]
    
    def recurent(t0,N10,N20):
        dt = 0.005
        dN1 = 0
        dN2 = 0
        
        t = np.arange(t0,tmax,dt)
        N1 = []
        N2 = []
        
        n1 = N10
        n2 = N20
        
        for x in t:
            n1 += dN1
            n2 += dN2
            
            N1.append(n1)
            N2.append(n2)
            
            dN1 = dt * fN1(n1,n2)
            dN2 = dt * fN2(n1,n2)
            
        return t, np.array(N1), np.array(N2)
        
    t0 = 0
    N10 = 3
    N20 = 1
    
    x,y1,y2 = recurent(t0,N10,N20)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,1)
    
    N1N2T = fig.add_subplot(gs[1,0])
    N1N2T.plot(x,y1,label="N1",c='g')
    N1N2T.plot(x,y2,label="N2",c='r')
    N1N2T.set_xlim(t0,tmax)
    N1N2T.legend()
    
    phase_space = fig.add_subplot(gs[0,0])
    Y1,Y2 = np.meshgrid(np.linspace(-1,10,50),np.linspace(-1,6,50))
    u,v = np.zeros(Y1.shape),np.zeros(Y2.shape)
    
    for i in range(Y1.shape[0]):
        for j in range(Y1.shape[1]):
            u[i, j],v[i,j] = fN1(Y1[i,j],Y2[i,j]), fN2(Y1[i,j],Y2[i,j])
    
    phase_space.quiver(Y1,Y2,u,v,width=0.0005)
    
    for i in range(10):
        tspan = np.arange(t0,10*tmax,0.01)
        y0 = [random.random()*5, random.random()*5]
        ys = odeint(f, y0, tspan)
        phase_space.plot(ys[:,0], ys[:,1], '-') # path
        phase_space.plot([ys[0,0]], [ys[0,1]], 'o') # start
        phase_space.plot([ys[-1,0]], [ys[-1,1]], 's') # end
    
    plt.show()

    
if __name__ == "__main__":
	Lab4_3()
