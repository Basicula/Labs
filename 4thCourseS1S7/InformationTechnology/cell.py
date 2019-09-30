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
		self.required = True
		
	@property
	def __dict__(self):
		return {
				'data' : self.data,
				'type' : self.type
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