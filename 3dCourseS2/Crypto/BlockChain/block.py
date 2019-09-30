from transaction import Transaction
import datetime
import hashlib
import json

class Block:
	def __init__(self,index,prev_hash,transactions,nonce = 0):
		self.index = index
		self.prev_hash = prev_hash
		self.transactions = transactions
		self.nonce = nonce
		
		self.timestamp = str(datetime.datetime.now())
		
		self.hash = self.calculateHash(self)
		
	@staticmethod
	def calculateHash(block):
		block_string = str(block.index) + str(block.nonce) + block.prev_hash + str(block.timestamp)
		for transaction in block.transactions:
			block_string += str(transaction)
		return hashlib.sha256(block_string.encode()).hexdigest()
		
	@property
	def __dict__(self):
		return {'index' : self.index,
				'prev_hash' : self.prev_hash,
				'hash' : self.hash,
				'nonce' : self.nonce,
				'time' : self.timestamp,
				'transactions' : self.transactions
				}
				
	@staticmethod
	def from_dict(dict):
		index = dict['index']
		prev_hash = dict['prev_hash']
		hash = dict['hash']
		nonce = dict['nonce']
		timestamp = dict['time']
		transactions = []
		for transaction in dict['transactions']:
			transactions.append(Transaction.from_dict(transaction))
		block = Block(index,prev_hash,transactions,nonce)
		block.hash = hash
		block.timestamp = timestamp
		return block
	
	def __repr__(self):
		return {
				'block_index' : self.index,
				'previous_hash' : self.prev_hash,
				'nonce' : self.nonce,
				'timestamp' : str(self.timestamp),
				'transactions' : self.transactions,
				}
		