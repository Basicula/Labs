from datatype import *

def isInteger(data):
	try:
		int(data)
	except ValueError:
		return False
	return True
	
def isReal(data):
	try:
		float(data)
	except ValueError:
		return False
	return True

def isChar(data):
	try:
		char(data)
	except ValueError:
		return False
	return True

class Cell:
	def __init__(self,data="",type=DataType.String):
		self.data = data
		self.type = type
		self.optionalInfo = None
		self.required = True
		
	def isPresentData(self):
		return self.data != ""
		
	def setData(self,data):
		if not Cell.isValidData(data,self.type):
			raise Exception("Invalid data for current cell")
		self.data = data
		
	@property
	def __dict__(self):
		if self.optionalInfo == None:
			return {
					'data' : self.data,
					'type' : self.type
					}
		else:
			return {
					'data' : self.data,
					'type' : self.type,
					self.optionalInfo[0] : self.optionalInfo[1]
					}
		
	@staticmethod
	def fromDict(dict):
		return Cell(dict['data'], DataType.fromDict(dict['type']))
	
	@staticmethod
	def isValidData(data,type):
		if type == DataType.Integer:
			return isInteger(data)
		elif type == DataType.Real:
			return isReal(data)
		elif type == DataType.Char:
			return isChar(data)
		elif type == DataType.String:
			return True
		else:
			return False