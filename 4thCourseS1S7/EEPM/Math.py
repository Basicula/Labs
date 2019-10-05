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
	def __init__(self,xs,ys,mode=0):
		self.additions = []
		self.eps = 0.01
		self.xs = xs
		self.ys = ys
		self.n = len(xs)
		self.mode = mode
		self.a = []
		
	def derivative(self):
		res = Polynom([],[])
		for i in range(1,len(self.a)):
			res.a.append(i*self.a[i])
		return res
		
	def intersection(self,other,interval):
		def sub(x):
			return self(x) - other(x)
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
				
	def strApproximation(self):
		if self.mode == 0:
			precision = int(len(self.a))
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
			return res
		elif self.mode == 1:
			precision = 3
			res = doubleToStr(self.a[0],precision) + " + " + doubleToStr(self.a[1]) + "*ln(x)"
			return res
		elif self.mode == 2:
			precision = 3
			res = doubleToStr(self.a[0],precision) + " * x^" + doubleToStr(self.a[1])
			return res

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
		
	def logarithmicApproximation(self):
		self.mode = 1
		matrix = []
		ys = []
		for i in range(2):
			row = []
			for j in range(2):
				t = 0
				for x in self.xs:
					t += np.log(x)**(i+j)
				row.append(t)
			matrix.append(row)
				
			y = 0
			for j in range(self.n):
				y += self.ys[j] * np.log(self.xs[j])**i
			ys.append(y)
		self.a = solveMatrixEquation(matrix,ys)

	def stepwiseApproximation(self):
		self.mode = 2
		matrix = []
		ys = []
		for i in range(2):
			row = []
			for j in range(2):
				t = 0
				for x in self.xs:
					t += np.log(x)**(i+j)
				row.append(t)
			matrix.append(row)
				
			y = 0
			for j in range(self.n):
				y += np.log(self.ys[j]) * np.log(self.xs[j])**i
			ys.append(y)
		self.a = solveMatrixEquation(matrix,ys)
		self.a[0] = np.e**self.a[0]
		
	def __call__(self,x):
		if self.mode == 0:
			res = 0
			for i in range(len(self.a)):
				res += self.a[i] * x**i
			return res
		elif self.mode == 1:
			return self.a[0] + self.a[1] * np.log(x)
		elif self.mode == 2:
			return self.a[0]*x**self.a[1]
		else:
			res = self.a[0]
			for i in range(1,len(self.a)):
				t = 1
				for j in range(i):
					t*=x-self.x[j]
				res += t * self.a[i]
			return res