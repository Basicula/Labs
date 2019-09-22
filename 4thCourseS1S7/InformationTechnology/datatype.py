from enum import Enum

class DataType(Enum):
	Integer = 0
	Real = 1
	Char = 2
	String = 3
	
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
			
	@staticmethod
	def asList():
		return ["Integer","Real","Char","String"]