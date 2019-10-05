import matplotlib.pyplot as plt

import sys
sys.path.append('..')

from Math import *			
			
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
	def createDefaultSubPlot(title=""):
		fig = plt.figure(constrained_layout=True)
		gs = fig.add_gridspec(1,1)
		
		res = fig.add_subplot(gs[0,0])
		
		res.set_title(title)
		res.set_xlabel("Quantity")
		res.set_ylabel("Price")
		
		return res
		
	def plotInputData(self):		
		inputData = Market.createDefaultSubPlot("Input data")
		
		inputData.scatter(self.demands,self.prices,s=10,c=self.demandColor)
		inputData.plot(self.demands,self.prices,label="demand data",c=self.demandColor)
		
		inputData.scatter(self.supplies,self.prices,s=10,c=self.supplyColor)
		inputData.plot(self.supplies,self.prices,label="supply data",c=self.supplyColor)
		
		inputData.legend()
		
	def preprocessAproximation(self,demand_type,supply_type):
		title = ""
		if demand_type == 0:
			title += "Polynomical" + str(self.approximationPower)
		elif demand_type == 1:
			title += "Logarithmic"
		elif demand_type == 2:
			title += "Stepwise"
		title += " and "
		if supply_type == 0:
			title += "Polynomical" + str(self.approximationPower)
		elif supply_type == 1:
			title += "Logarithmic"
		elif supply_type == 2:
			title += "Stepwise"
			
		self.demandCurve = Polynom(self.prices,self.demands)
		if demand_type == 0:
			self.demandCurve.polynomicalApproximation(self.approximationPower)
		elif demand_type == 1:
			self.demandCurve.logarithmicApproximation()
		elif demand_type == 2:
			self.demandCurve.stepwiseApproximation()
			
		self.supplyCurve = Polynom(self.prices,self.supplies)
		if supply_type == 0:
			self.supplyCurve.polynomicalApproximation(self.approximationPower)
		elif supply_type == 1:
			self.supplyCurve.logarithmicApproximation()
		elif supply_type == 2:
			self.supplyCurve.stepwiseApproximation()
			
		return title
		
	#type: 0 - polynomicalApproximation, 1 - logarithmicApproximation, 2 - stepwiseApproximation
	def plotApproximation(self,demand_type=0,supply_type=0,i_aproximatedData = None):	
		mid_val = self.xrange[self.xrange.shape[0]//2]
		
		title = self.preprocessAproximation(demand_type,supply_type)
	
		aproximatedData = i_aproximatedData
		if aproximatedData == None:
			aproximatedData = Market.createDefaultSubPlot(title)
		
		aproximatedData.scatter(self.demandCurve(self.xrange),
								self.xrange,
								c=grad(self.demandColor,len(self.xrange)),
								s=5)
		aproximatedData.scatter(self.demandCurve(mid_val),
								mid_val,
								c=self.demandColor,
								s=5,
								label=self.demandCurve.strApproximation())
		aproximatedData.scatter(self.supplyCurve(self.xrange),
								self.xrange,
								c=grad(self.supplyColor,len(self.xrange),True),
								s=5)
		aproximatedData.scatter(self.supplyCurve(mid_val),
								mid_val,
								c=self.supplyColor,
								s=5,
								label=self.supplyCurve.strApproximation())
		
		if self.isShowKeyPoints:
			aproximatedData.scatter(self.demands,self.prices,s=10,c=self.demandColor)
			aproximatedData.scatter(self.supplies,self.prices,s=10,c=self.supplyColor)
			
		if self.isShowIntersection:
			self.balance = self.demandCurve.intersection(self.supplyCurve,[min(self.prices),max(self.prices)])
			balance_quantity = self.demandCurve(self.balance)
			lbl = "(" + doubleToStr(self.balance,4) + ", " + doubleToStr(balance_quantity,4) + ")"
			aproximatedData.scatter(balance_quantity,self.balance,c='r',label=lbl)

		aproximatedData.legend()
		
	def plotApproximationsCompare(self):
		fig = plt.figure(constrained_layout=True)
		gs = fig.add_gridspec(3,3)
		
		for d_t in range(3):
			for s_t in range(3):
				title = self.preprocessAproximation(d_t,s_t)
				
				ax = fig.add_subplot(gs[d_t,s_t])
				ax.set_title(title)
				ax.set_xlabel("Quantity")
				ax.set_ylabel("Price")
				
				self.plotApproximation(d_t,s_t,ax)
		
	def plotWithGrant(self):
		aproximatedData = Market.createDefaultSubPlot("With grant")
		
		self.demandCurve = Polynom(self.prices,self.demands)
		self.demandCurve.polynomicalApproximation(self.approximationPower)
		aproximatedData.scatter(self.demandCurve(self.xrange),self.xrange,c=grad(self.demandColor,len(self.xrange)),s=5)
		
		self.supplyCurve = Polynom(self.prices,self.supplies)
		self.supplyCurve.polynomicalApproximation(self.approximationPower)
		aproximatedData.scatter(self.supplyCurve(self.xrange),self.xrange,c=grad(self.supplyColor,len(self.xrange),True),s=5)
		
		self.grantCurve = Polynom(np.array(self.prices)-self.grant,self.supplies)
		self.grantCurve.polynomicalApproximation(self.approximationPower)
		aproximatedData.scatter(self.grantCurve(self.xrange),self.xrange,c=grad(self.supplyColor,len(self.xrange),True),s=5)
		
		if self.isShowIntersection:
			self.balance = self.demandCurve.intersection(self.supplyCurve,[min(self.prices),max(self.prices)])
			self.grantBalance = self.demandCurve.intersection(self.grantCurve,[min(self.prices),max(self.prices)])
			aproximatedData.scatter(self.demandCurve(self.balance),self.balance,c='r')	
			aproximatedData.scatter(self.demandCurve(self.grantBalance),self.grantBalance,c='r')
	
	def printInfo(self):
		p = self.prices
		d = self.demands
		s = self.supplies
		
		print("\n---Market status---\n")
		
		print(self.demandCurve.strApproximation())
		print(self.supplyCurve.strApproximation())
		
		t = self.balance
		print("Balance point with price = ",t)
		print("Ed = ",abs(self.demandCurve.derivative()(t)*t/self.demandCurve(t)))
		print("Es = ",abs(self.supplyCurve.derivative()(t)*t/self.supplyCurve(t)))
		t = self.grantBalance
		print("Balance point with grant = ",t)
		print("Ed = ",abs(self.demandCurve.derivative()(t)*t/self.demandCurve(t)))
		print("Es = ",abs(self.grantCurve.derivative()(t)*t/self.grantCurve(t)))
		
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
	market.plotInputData()
	market.plotApproximationsCompare()
	market.plotWithGrant()
	market.printInfo()
	
	plt.show()
