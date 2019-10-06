import numpy
from matplotlib.pylab import *
g = 9.81

# E.8 a)
def forwardEuler(f, N, T, uk):
    dt = float(T) / N
    for i in range(N):
        tk = i * dt
        yield [tk, uk]
        uk = uk + dt * f(uk, tk)

class FluidBody(object):
    def __init__(self, sigma, sigma_b, A, V, C_D):
        self.sigma = sigma
        self.sigma_b = sigma_b
        self.A = A
        self.V = V
        self.C_D = C_D
        self.g = g

    def fluid(self, uk, tk):
        g = self.g
        sigma = self.sigma
        sigma_b = self.sigma_b
        A = self.A
        V = self.V
        C_D = self.C_D
        return -g * (1 - sigma / sigma_b) - 0.5 * C_D * sigma * A / (sigma_b * V) * abs(uk) * uk


    def __call__(self, uk, tk):
        return self.fluid(uk, tk)

# E.8 b)
def test_linear():
    fb = FluidBody(0.0, 1.0, 1.0, 1.0, 1.0)
    tks = []
    uks = []
    ratios = []
    olduk = 0
    k = 1.0
    eps = 1.0E-7
    allok = True
    for [tk, uk] in forwardEuler(fb, 100, 10.0, olduk):
        expected = (olduk - g * k * tk)
        if not((uk - expected) < eps):
            print( uk, expected)
            allok = False
    if allok:
        print ('all good and linear')

# E.8 c)
# The graph shows F_g and F_b as constant while F_d decreases towards 0.
def plot_forces():
    fb = FluidBody(0.79, 1003.0, 0.9, 0.08, 0.6)
    sigma = fb.sigma
    sigma_b = fb.sigma_b
    A = fb.A
    V = fb.V
    C_D = fb.C_D
    m = sigma_b * V
    F_g = -m * g
    F_d = lambda uk, tk: -0.5 * C_D * sigma * A * abs(uk) * uk
    F_b = sigma * g * V
    x = []
    y = []
    olduk = 50.0
    N = 100
    T = 1.0
    for [tk, uk] in forwardEuler(F_d, N, T, olduk):
        x.append(tk)
        y.append(uk)
    plot(x, y, 'r-')
    plot(x, [F_g for _ in y], 'g-')
    plot(x, [F_b for _ in y], 'b-')
    show()

# E.8 d)
# The graph shows velocity converging to ~-60 m/s
def plot_skydiver():
    fb = FluidBody(sigma=0.79, sigma_b=1003.0, A=0.9, V=0.08, C_D=0.6)
    N = 100
    T = 20.0
    olduk = 0.0
    x = []
    y = []
    for [tk, uk] in forwardEuler(fb, N, T, olduk):
        print( tk, uk)
        x.append(tk)
        y.append(uk)
    plot(x, y, 'b-')
    show()

# E.8 e)
# The graph shows velocity converging to ~3.64 m/s
def plot_ball():
    r = 0.11
    m = 0.43
    V = 4.0/3.0*pi*r**3
    sigma_b = m / V
    print(V,sigma_b,pi*r**2)
    fb = FluidBody(sigma=1000.0, sigma_b=sigma_b, A=pi*r**2, V=V, C_D=0.2)
    N = 1000
    T = 1.0
    olduk = 0.0
    x = []
    y = []
    for [tk, uk] in forwardEuler(fb, N, T, olduk):
        x.append(tk)
        y.append(uk)
    plot(x, y, 'b-')
    show()

def main():
    'entry point'
    #test_linear()
    #plot_forces()
    #plot_skydiver()
    plot_ball()

    #plot(tks, uks)
    #show()

if __name__ == '__main__':
    main()
