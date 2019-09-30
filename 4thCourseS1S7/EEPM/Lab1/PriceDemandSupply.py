import matplotlib.pyplot as plt
import numpy as np

def doubleToStr(a,prec=3):
	regex = "{0:."+str(prec)+"f}"
	return regex.format(round(a,prec))
	
def toHex(a):
	return '#{0:02x}{1:02x}{2:02x}'.format(int(a[0]),int(a[1]),int(a[2]))

def grad(color,n,inv=False):
	if isinstance(color,str):
		color = color[1:]
		color = [int(color[i:i+2],16) for i in range(0,len(color),2)]
	colors = []
	for i in range(n):
		c = ""
		if i < n/2:
			t = 2*i/n
			c = toHex([color[0]*t,color[1]*t,color[2]*t])
		else:
			t = (i - n/2) / (n - n/2)
			c = toHex([color[0] + (255 - color[0])*t,color[1] + (255 - color[1])*t,color[2] + (255 - color[2])*t])
		colors.append(c)
	if inv:
		return list(reversed(colors))
	return colors

def solveMatrixEquation(matrix,b):
	n = len(b)
	for i in range(n):
		t = matrix[i][i]
		for j in range(n):
			matrix[i][j] /= t
		b[i] /= t
	
		for j in range(n):
			if j == i:
				continue
			t = matrix[j][i]
			for k in range(i,n):
				matrix[j][k] -= matrix[i][k] * t
			b[j] -= b[i] * t
	return b

class Polynom:
	def __init__(self,xs,ys):
		self.additions = []
		self.eps = 0.01
		self.xs = xs
		self.ys = ys
		self.n = len(xs)
		self.mode = 0
		self.a = []
		
	def __sub__(self,other):
		res = Polynom([],[])
		if len(self.a) == len(other.a):
			for i in range(len(self.a)):
				res.a.append(self.a[i] - other.a[i])
		return res
		
	def derivative(self):
		res = Polynom([],[])
		for i in range(1,len(self.a)):
			res.a.append(i*self.a[i])
		return res
		
	def intersection(self,other,interval):
		sub = self - other
		if sub(interval[0]) * sub(interval[1]) <= 0:
			l = interval[0]
			r = interval[1]
			prev = sub(l)
			while l < r:
				m = (l+r)/2
				curr = sub(m)
				if abs(curr-prev) < 1e-4:
					return m
				elif sub(l)*sub(m) < 0:
					r = m
				elif sub(m)*sub(r) < 0:
					l = m
				else:
					return None
				prev = curr
		else:
			m = (interval[0]+interval[1])/2
			l = self.intersection(other,[interval[0],m])
			r = self.intersection(other,[m,interval[1]])
			if l != None:
				return l
			elif r != None:
				return r
		return None
		
	def NewtonPolynomial(self):
		self.a = []
		for y in ys:
			self.a.append(y)
		
		for i in range(1,n):
			for j in range(n-1,i-1,-1):
				self.a[j] = (self.a[j] - self.a[j-1])/(self.x[j] - self.x[j-i])
				
	def printApproximation(self):
		precision = int(len(self.a)/2)
		res = doubleToStr(self.a[0],precision)
		for i in range(1,len(self.a)):
			if self.a[i] == 0:
				continue
			elif self.a[i] < 0:
				res += " - "
			else:
				res += " + "
			res += doubleToStr(abs(self.a[i]),precision)+"*x"
			if i > 1:
				res += "^"+str(i)
		print(res)

	def polynomicalApproximation(self,power):
		self.mode = 0
		power+=1
		matrix = []
		ys = []
		for i in range(power):
			row = []
			for j in range(power):
				t = 0
				for x in self.xs:
					t+=x**(i+j)
				row.append(t)
			matrix.append(row)
			
			y = 0
			for j in range(self.n):
				y += self.ys[j] * self.xs[j]**i
			ys.append(y)	
		self.a = solveMatrixEquation(matrix,ys)
		
	def __call__(self,x):
		if self.mode == 1:
			res = self.a[0]
			for i in range(1,len(self.a)):
				t = 1
				for j in range(i):
					t*=x-self.x[j]
				res += t * self.a[i]
			return res
		else:
			res = 0
			for i in range(len(self.a)):
				res += self.a[i] * x**i
			return res
			
class Market:
	def __init__(self,prices,demands,supplies,grant):
		self.prices = prices
		self.demands = demands
		self.supplies = supplies
		self.grant = grant
		
		self.demandColor = '#0000ff'
		self.supplyColor = '#ffa500'
		
		self.isShowKeyPoints = True
		self.isShowIntersection = True
		
		self.approximationPower = 2;
		
		self.step = 0.05
		self.xrange = np.arange(min(self.prices)-self.step,max(self.prices)+self.step,self.step)

	@staticmethod
	def createDefaultSubPlot(fig,gs,row,column,title=""):
		res = fig.add_subplot(gs[row,column])
		
		res.set_title(title)
		res.set_xlabel("Quantity")
		res.set_ylabel("Price")
		
		return res
		
	def marketPlot(self):
		fig = plt.figure(constrained_layout=True)
		gs = fig.add_gridspec(2,1)
		
		inputData = Market.createDefaultSubPlot(fig,gs,0,0,"Input data")
		
		inputData.scatter(self.demands,self.prices,s=10,c=self.demandColor)
		inputData.plot(self.demands,self.prices,label="demand data",c=self.demandColor)
		
		inputData.scatter(self.supplies,self.prices,s=10,c=self.supplyColor)
		inputData.plot(self.supplies,self.prices,label="supply data",c=self.supplyColor)
		
		inputData.legend()
		
		self.addMainApproximation(fig,gs,1,0)
		
	def addMainApproximation(self,fig,gs,row,column):
		aproximatedData = Market.createDefaultSubPlot(fig,gs,row,column)
		
		self.demandCurve = Polynom(self.prices,self.demands)
		self.demandCurve.polynomicalApproximation(self.approximationPower)
		aproximatedData.scatter(self.demandCurve(self.xrange),self.xrange,c=grad(self.demandColor,len(self.xrange)),s=5)
		
		self.supplyCurve = Polynom(self.prices,self.supplies)
		self.supplyCurve.polynomicalApproximation(self.approximationPower)
		aproximatedData.scatter(self.supplyCurve(self.xrange),self.xrange,c=grad(self.supplyColor,len(self.xrange),True),s=5)
		
		self.grantCurve = Polynom(np.array(self.prices)-self.grant,self.supplies)
		self.grantCurve.polynomicalApproximation(self.approximationPower)
		aproximatedData.scatter(self.grantCurve(self.xrange),self.xrange,c=grad(self.supplyColor,len(self.xrange),True),s=5)
		
		self.grantCurve2 = Polynom(self.prices,np.array(self.supplies)+2*self.grant)
		self.grantCurve2.polynomicalApproximation(self.approximationPower)
		aproximatedData.scatter(self.grantCurve2(self.xrange),self.xrange,c=grad(self.supplyColor,len(self.xrange),True),s=5)
		
		if self.isShowIntersection:
			self.balance = self.demandCurve.intersection(self.supplyCurve,[min(self.prices),max(self.prices)])
			self.grantBalance = self.demandCurve.intersection(self.grantCurve,[min(self.prices),max(self.prices)])
			self.grantBalance2 = self.demandCurve.intersection(self.grantCurve2,[min(self.prices),max(self.prices)])
			aproximatedData.scatter(self.demandCurve(self.balance),self.balance,c='r')	
			aproximatedData.scatter(self.demandCurve(self.grantBalance),self.grantBalance,c='r')	
			aproximatedData.scatter(self.demandCurve(self.grantBalance2),self.grantBalance2,c='r')	
		
	def addPolynomicalApproximation(self,fig,gs,row,column,power):
		p = self.prices
		d = self.demands
		s = self.supplies
	
		aproximatedData = Market.createDefaultSubPlot(fig,gs,row,column,"Approximation power "+str(power))
		
		demandCurve = Polynom(p,d)
		demandCurve.polynomicalApproximation(power)
		aproximatedData.scatter(demandCurve(self.xrange),self.xrange,c=grad(self.demandColor,len(self.xrange)),s=5)
		
		supplyCurve = Polynom(p,s)
		supplyCurve.polynomicalApproximation(power)
		aproximatedData.scatter(supplyCurve(self.xrange),self.xrange,c=grad(self.supplyColor,len(self.xrange),True),s=5)
		
		if self.isShowKeyPoints:
			aproximatedData.scatter(d,p,s=10,c=self.demandColor)
			aproximatedData.scatter(s,p,s=10,c=self.supplyColor)
			
		if self.isShowIntersection:
			self.balance = demandCurve.intersection(supplyCurve,[min(p),max(p)])
			aproximatedData.scatter(demandCurve(self.balance),self.balance,c='r')			
	
		
	def marketApproximation(self):
		fig = plt.figure(constrained_layout=True)
		gs = fig.add_gridspec(3,3)
		
		for pw in range(9):
			self.addPolynomicalApproximation(fig,gs,pw%3,pw//3,pw+1)
	
	def printInfo(self):
		p = self.prices
		d = self.demands
		s = self.supplies
		
		print("\n---Market status---\n")
		
		self.demandCurve.printApproximation()
		self.supplyCurve.printApproximation()
		
		t = self.balance
		print("Balance point with price = ",t)
		print("Ed = ",abs(self.demandCurve.derivative()(t)*t/self.demandCurve(t)))
		print("Es = ",abs(self.supplyCurve.derivative()(t)*t/self.supplyCurve(t)))
		t = self.grantBalance
		print("Balance point with grant = ",t)
		print("Ed = ",abs(self.demandCurve.derivative()(t)*t/self.demandCurve(t)))
		print("Es = ",abs(self.grantCurve.derivative()(t)*t/self.grantCurve(t)))
		t = self.grantBalance2
		print("Balance point with grant = ",t)
		print("Ed = ",abs(self.demandCurve.derivative()(t)*t/self.demandCurve(t)))
		print("Es = ",abs(self.grantCurve2.derivative()(t)*t/self.grantCurve2(t)))
		
		separ = "\t"
		prices = "Prices\t"
		demands = "Demands\t"
		supplies = "Supplies"
		for i in range(len(p)):
			prices += separ + str(p[i])
			demands += separ + str(d[i])
			supplies += separ + str(s[i])
		
		ed_curve = "Ed curve"
		es_curve = "Es curve"
		for i in range(1,len(p)):
			ed_curve += separ + doubleToStr((d[i] - d[i-1]) * (p[i] + p[i-1]) / ((p[i] - p[i-1]) * (d[i] + d[i-1])))
			es_curve += separ + doubleToStr((s[i] - s[i-1]) * (p[i] + p[i-1]) / ((p[i] - p[i-1]) * (s[i] + s[i-1])))
			
		print(prices)
		print(demands)
		print(supplies)
		print(ed_curve)
		print(es_curve)

if __name__ == "__main__":
	prices 	= [3,	4.1,	5.1,	6,	6.8,	7.5,	8.8,	9.4,	10,	11,	11.8,	12.2]
	demands = [116,	90,		74,		63,	53,		43,		38,		32,		29,	25,	24,		18]
	supplies = [1,	3,		11,		16,	19,		21,		22,		25,		30,	32,	35,		41]
	
	market = Market(prices,demands,supplies,2)
	market.marketPlot()
	market.marketApproximation()
	market.printInfo()
	
	plt.show()
