from enum import Enum

class DataType(Enum):
	Integer = 0
	Real = 1
	Char = 2
	String = 3
	Picture = 4
	RealInvl = 5
	
	def defaultValue(self):
		if self == DataType.Integer:
			return 0
		elif self == DataType.Real:
			return 0.0
		elif self == DataType.Char:
			return ''
		elif self == DataType.String:
			return ''
		elif self == DataType.Picture:
			return None
		elif self == DataType.RealInvl:
			return [0.0,1.0]
	
	@property
	def __dict__(self):
		if self == DataType.Integer:
			return "integer"
		elif self == DataType.Real:
			return "real"
		elif self == DataType.Char:
			return "char"
		elif self == DataType.String:
			return "string"
		elif self == DataType.Picture:
			return "picture"
		elif self == DataType.RealInvl:
			return "realinvl"
			
	@staticmethod
	def fromDict(dict):
		if dict == "integer":
			return DataType.Integer
		elif dict == "real":
			return DataType.Real
		elif dict == "char":
			return DataType.Char
		elif dict == "string":
			return DataType.String
		elif self == "picture":
			return DataType.Picture
		elif self == "realinvl":
			return DataType.RealInvl
			
	@staticmethod
	def asList():
		return ["Integer","Real","Char","String","Picture","RealInvl"]