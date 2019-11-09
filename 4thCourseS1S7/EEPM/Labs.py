import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

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
    
    
if __name__ == "__main__":
	Lab4_1()
