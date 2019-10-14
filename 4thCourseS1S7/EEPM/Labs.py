import matplotlib.pyplot as plt
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

if __name__ == "__main__":
	Lab1()
