import numpy as np
import matplotlib.pyplot as plt
import enum
import math

class DifferentialMethod(enum.Enum):
	ForwardEuler = 0
	FrowardHeun = 1


class cont:
	def __init__(self,t,x):
		self.t = t
		self.x = x
		
	def __call__(self,t):
		i = 0
		while i < len(self.t) and t > self.t[i]:
			i+=1
		if i ==  len(self.t) - 1:
			return self.x[i]
		else:
			return (self.x[i] + self.x[i+1])/2

def BodyInFluid(u, t, ro_fluid, ro_body, body_volume, cross_section_area, drag_coef):
	rf_rb = ro_fluid / ro_body
	return -9.8 * (1 - rf_rb) - 0.5 * drag_coef * cross_section_area * rf_rb / body_volume * abs(u) * u	

def ForwardApproach(func,initial_state,x_segment,num_iterations=100,method=DifferentialMethod.ForwardEuler):
	u = np.zeros(num_iterations+1)
	t = np.zeros(num_iterations+1)
	u[0] = initial_state
	dt = (x_segment[1] - x_segment[0])/num_iterations
	for i in range(num_iterations):
		t[i+1] = t[i] + dt
		fi = func(u[i],t[i])
		if method == DifferentialMethod.ForwardEuler:
			u[i+1] = u[i] + dt * fi
		elif method == DifferentialMethod.FrowardHeun:
			tempu = u[i] + dt * fi
			u[i+1] = u[i] + dt * fi / 2 + dt * func(tempu,t[i+1])/2	
			
	return u,t
	
def PlotResult(u,t):
	plt.plot(t,u)

if __name__ == '__main__':
	dsquarey = lambda u,t: 2*t
	grows_of_population = lambda u,t,alpha=0.2,R=10:alpha*u*(1-u/R)
	body_in_fluid_zero_ro = lambda u,t : BodyInFluid(u,t,0,1,1,1,1)
	skydiver_in_free_fall = lambda u,t : BodyInFluid(u,t,0.79,1003.0,0.08,0.9,0.6)
	m = 0.43
	r = 0.06
	v = 4 * math.pi * r**3 / 3
	ball_in_water = lambda u,t : BodyInFluid(u,t,1000,m/v,v,math.pi*r**2,0.4)
	vu,vt = ForwardApproach(ball_in_water,0,[0,2],1000)
	velocity = cont(vt, vu)
	ball_in_water_2 = lambda y,t : velocity(t)
	#for num_iterations in [100,1000,10000]:
	u,t = ForwardApproach(ball_in_water_2,-10,[0,1],1000)
	PlotResult(u,t)
		
	plt.show()
