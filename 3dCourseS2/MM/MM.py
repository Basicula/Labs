import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import math
from collections import namedtuple

State = namedtuple("State","x,t")
System = namedtuple("System","dimension,x_range,t_range")
g_max_integer = 50

def H(x):
	return int(x>0)

class Simulation:
	'''GetRandomInBoxRanges
	Help function for getting random point in space in simulating system
	'''
	def GetRandomInBoxRanges(self):
		x = []
		ranges = self.system.x_range
		for dim in range(self.system.dimension):
			x += [random.uniform(ranges[dim][0],ranges[dim][1])]
		return x
	#end GetRandomInBoxRanges
	
	'''GetRandomOutBoxRanges
	Help function for getting random point in space out simulating system
	'''
	def GetRandomOutBoxRanges(self):
		out_ranges = []
		ranges = self.system.x_range
		for dim in range(self.system.dimension):
			mx = max(abs(ranges[dim][0]),abs(ranges[dim][1]))*10
			out_ranges += [[[-mx,ranges[dim][0]],[ranges[dim][1],mx]]]
		x = []
		for dim in range(self.system.dimension):
			l_or_r = random.randint(0,1)
			x += [random.uniform(out_ranges[dim][l_or_r][0],out_ranges[dim][l_or_r][1])]
		return x
	#end GetRandomOutBoxRanges

	'''InitSystem
	Init system where:
		1. dimensions count for space 1D 2D 3D and so on
		2. ranges for every dimension 
		3. time range 
	self.system = System(1,[[0,50]],[0,50])
	'''
	def InitSystem(self,dimension_count,space_ranges,time_range):
		self.system = System(dimension_count,space_ranges,time_range)
	#end InitSystem
	
	'''SetMainFunction
	Init function y(x,t) = y(s)
	'''
	def SetMainFunction(self,function):
		self.y = function
	#end SetMainFunction
	
	'''SetUFunction
	Init u where u(s) = Ly(x,t) = Ly(s)
	'''
	def SetUFunction(self,function):
		self.u = function
	#end SetUFunction
	
	'''SetGreen_sFunction
	Init G Green's function G(s,ss)
	'''
	def SetGreen_sFunction(self,function):
		self.g = function
	#end SetGreen_sFunction
	
	'''InitZeroTimeData
	Init data for finding zero-time values(y(x,0))
		self.R0 - count for different L, 1 by default
		self.L0 - count for points with zero time
		self.S0 - zero-time states s = (x,0)
		self.Y0 - result vector for zero-time task
	'''
	def InitZeroTimeData(self):
		self.R0 = 1
		self.L0 = 0
		self.S0 = []
		self.Y0 = []
	#end InitZeroTimeData
		
	'''AddZeroTimeStates
	Function for adding new zero-time states 
	where state = State(x,t) and x - K-dimensional point in ranges and t in ranges
	'''
	def AddZeroTimeStates(self,states):
		self.L0 += len(states)
		self.S0 += states
		for state in states:
			self.Y0 += [self.y(state)]
	#end AddZeroTimeStates
		
	'''InitContourData
	Init data for finding values(y(x,t)) where x on range's contours
		self.RG - count for different L, 1 by default
		self.LG - count for such points
		self.SG - such states
		self.YG - result vector in such points
	'''
	def InitContourData(self):
		self.RG = 1
		self.LG = 0
		self.SG = []
		self.YG = []
	#end InitContourData
	
	'''AddContourStates
	Function for adding contour states
	where state = State(x,t), x - K-dimensional point on range's contour and t from time range
	'''
	def AddContourStates(self,states):
		self.LG += len(states)
		self.SG += states
		for state in states:
			self.YG += [self.y(state)]
	#end AddContourStates
	
	'''InitMStatesData
	Points that will be taken from user
	or randomly generated
	'''
	def InitMStatesData(self):
		self.M_cnt	= 0
		self.M0_cnt = 0 
		self.MG_cnt = 0
		
		self.M 	= []
		self.M0 = []
		self.MG = []
	#end InitMPointsData
	
	'''AddMStates
	M state - state where x is in ranges and time is in range
	'''
	def AddMStates(self,points):
		self.M_cnt += len(points)
		self.M += points
	#end AddMStates
	
	'''GenerateMStates
	Function for generating random M states
	'''
	def GenerateMStates(self,count):
		self.M_cnt = count
		t_range = self.system.t_range
		for i in range(self.M_cnt):
			x = self.GetRandomInBoxRanges()
			t = random.uniform(t_range[0],t_range[1])
			self.M += [State(x,t)]
	#end GenerateMStates
	
	'''AddM0States
	M0 state - state where x in ranges and time is less or equal 0
	'''
	def AddM0States(self,points):
		self.M0_cnt += len(points)
		self.M0 += points
	#end AddM0States
	
	'''GenerateM0States
	Function for generating random M0 states
	'''
	def GenerateM0States(self,count):
		self.M0_cnt = count
		for i in range(self.M0_cnt):
			x = self.GetRandomInBoxRanges()
			t = random.uniform(-g_max_integer,0)
			self.M0 += [State(x,t)]
	#end GenerateM0States
	
	'''AddMGStates
	MG state - state where x is in out of ranges and time is in range
	'''
	def AddMGStates(self,points):
		self.MG_cnt += len(points)
		self.MG += points
	#end AddMGStates
	
	'''GenerateMGStates
	Function for generating random MG states
	'''
	def GenerateMGStates(self,count):
		self.MG_cnt = count
		t_range = self.system.t_range
		for i in range(self.MG_cnt):
			x = self.GetRandomOutBoxRanges()
			t = random.uniform(t_range[0],t_range[1])
			self.MG += [State(x,t)]
	#end GenerateMGStates
	
	'''CalculateMatrix
	Init A matrix
		self.A - matrix contains blocks A11,A12,A21,A22
		 |A11 A12|
		 |A21 A22|
		 A11 - S0 M0
		 A12 - S0 MG
		 A21 - SG M0
		 A22 - SG MG
	'''
	def CalculateMatrix(self):
		self.A = []
		for row_index in range(self.L0 + self.LG):
			row = []
			for column_index in range(self.M0_cnt + self.MG_cnt):
				state = None
				if column_index < self.M0_cnt: #A11 and A21
					state = self.M0[column_index]
				else: #A12 and A22
					state = self.MG[column_index - self.M0_cnt]
				if row_index < self.L0:
					row += [self.g(self.S0[row_index],state)] #A11 and A12
				else:
					row += [self.g(self.SG[row_index - self.L0],state)] #A21 and A22
			self.A += [row]
	#end CalculateMatrix
	
	'''CalculateUVectors
	U-vectors:
	U 	= (um) 	m 	in [0,M_cnt)
	U0 	= (um0) m0 	in [0,M0_cnt)
	UG 	= (umg) mg 	in [0,MG_cnt)
	'''
	def CalculateUVectors(self):
		self.U = []
		for i in range(self.M_cnt):
			self.U += [self.u(self.M[i])]
		Y = self.Y0 + self.YG
		A = np.array(self.A)
		P = np.dot(A,np.matrix.transpose(A))
		invP = np.linalg.inv(P)
		self.U0 = np.dot(np.matrix.transpose(A[:,:self.M0_cnt]),np.dot(invP,Y))
		self.UG = np.dot(np.matrix.transpose(A[:,self.M0_cnt:]),np.dot(invP,Y))
	#end CalculateUVectors
	
	'''Draw
	Build a plot
	'''
	def Draw(self):
		self.CalculateMatrix()
		self.CalculateUVectors()
		fig = plt.figure()
		ax = fig.add_subplot(111,projection='3d')
		ax.set_xlabel('x')
		ax.set_ylabel('time')
		ax.set_zlabel('val')
		points = []
		for x in np.linspace(self.system.x_range[0][0],self.system.x_range[0][1],50):
			for t in np.linspace(self.system.t_range[0],self.system.t_range[1],50):
				point = [x,t,self.CalculateResult(State([x],t))]
				points += [point]
				#ax.scatter(x[0],x[1],x[2])
		#points = np.array(sorted(np.array(points),key = lambda x : x[0] if x[0]!=x[1] else x[1] if x[1]!=x[2] else x[2]))
		points = np.array(points)
		#ax.plot(points[:,0],points[:,1],points[:,2])
		surf = ax.plot_trisurf(points[:,0],points[:,1],points[:,2],cmap = cm.jet,antialiased=False)
		s0 = []
		for state in self.S0:
			point = [state.x[0],state.t,self.CalculateResult(state)]
			s0 += [point]
		s0 = np.array(s0)
		ax.scatter(s0[:,0],s0[:,1],s0[:,2],c ='k',s = 30)
		fig.colorbar(surf)
		
		plt.show()
	#end Draw
	
	'''CalculateResult
	y(s) = yinf(s) + y0(s) + yg(s)
	'''
	def CalculateResult(self,state):
		res = 0
		for i in range(self.M_cnt):
			res += self.g(state,self.M[i]) 	* self.U[i]
		for i in range(self.M0_cnt):
			res += self.g(state,self.M0[i]) * self.U0[i]
		for i in range(self.MG_cnt):
			res += self.g(state,self.MG[i]) * self.UG[i]
		return res
	#end CalculateResult
	
	def __init__(self,dimension_count = 1,space_ranges = [0,50],time_range = [0,50]):
		self.InitSystem(dimension_count,space_ranges,time_range)
		
		self.InitZeroTimeData()
		self.InitContourData()
		
		self.InitMStatesData()
	#__init__ end
	
if __name__ == "__main__":
	simulation = Simulation(1,[[0,50]],[0,50])
	
	simulation.SetMainFunction(lambda s : 5 * math.sin(s.x[0]/5) + 4 * math.cos(s.t/4))
	simulation.SetUFunction(lambda s : -math.sin(s.x[0]/5) / 5 - math.cos(s.t/4) / 4)
	simulation.SetGreen_sFunction(lambda s,ss : 0 if s.x[0]==ss.x[0] and s.t == ss.t else np.log(1.0 / ((s.x[0] - ss.x[0]) * (s.x[0] - ss.x[0]) + (s.t - ss.t) * (s.t - ss.t))) / (2 * math.pi))
		
	S0 = []
	for i in range(0,30,2):
		S0 += [State([i],0)]
	simulation.AddZeroTimeStates(S0)
	
	#simulation.AddMStates(	[State([0],0),	State([10],10),	State([3],30),	State([40],40),	State([50],50)])
	simulation.AddM0States(	[State([1],-10),State([2],-20),	State([3],-30),	State([4],-1),	State([5],-2)])
	simulation.AddMGStates(	[State([100],1),State([200],30),State([55],10),	State([65],20),	State([75],30)])
	
	simulation.GenerateMStates(100)
	simulation.GenerateM0States(100)
	simulation.GenerateMGStates(100)
	
	simulation.CalculateMatrix()
	simulation.CalculateUVectors()
	simulation.Draw()




















