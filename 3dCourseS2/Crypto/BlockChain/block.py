import datetime

class Block:
	def __init__(self,index,prev_hash,nonce = 0):
		self.prev_hash = prev_hash
		self.index = index
		self.transactions = []
		self.nonce = nonce
		
		self.timestamp = datetime.datetime.now()
		
		self.header
		self.hash