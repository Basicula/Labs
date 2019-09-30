from cell import *

class Row:
	def __init__(self,cells):
		self.cells = cells
		
	@property
	def __dict__(self):
		return {
				'cells' : self.cells
				}
		
	@staticmethod
	def fromDict(dict):
		for cell in dict['cells']:
			self.cells.append(Cell.fromDict(cell))