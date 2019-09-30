import numpy as np
import matplotlib.pyplot as plt

import random
import timeit

def ZeroMatrix(n):
	res = [[0] * n for i in range(n)]
	return res

def IdentityMatrix(n):
	res = [[0] * n for i in range(n)]
	for i in range(n):
		res[i][i] = 1
	return res

def RandomMatrix(n):
	res = [[0] * n for i in range(n)]
	for i in range(n):
		for j in range(n):
			res[i][j] = random.randint(0,n)
	return res

def MultiplyMatrix(first,second):
	n = len(first)
	res = [[0] * n for i in range(n)]
	for i in range(n):
		for j in range(n):
			for k in range(n):
				res[i][j] += first[i][k]*second[k][j]
	return res
	
def Wrapper(first,second):
	def foo():
		c = MultiplyMatrix(first,second)
	return foo
	
def Analyse():
	times = []
	mx_n = 250
	for n in range(2,mx_n):
		z = ZeroMatrix(n)
		i = IdentityMatrix(n)
		a = RandomMatrix(n)
		b = RandomMatrix(n)
		c = MultiplyMatrix(z,b)
		t = timeit.Timer(Wrapper(a,b))
		times.append([n,t.timeit(1)])
	const = mx_n**3 / times[-1][1]
	x = np.arange(2,mx_n,1)
	y = x**3/const
	times = np.array(times)
	plt.plot(times[:,0],times[:,1],'g')
	plt.plot(x,y,'r')
	plt.savefig("2-250.png")
	
if __name__ == "__main__":
	Analyse()