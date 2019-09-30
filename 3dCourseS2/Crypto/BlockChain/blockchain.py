from block import Block
from transaction import Transaction, TransactionType
from collections import deque
import json
import hashlib

class BlockChain:
	def __init__(self):
		self.__transactions = deque()
		self.__chain = []
		self.__freeblocks = deque()
		self.__max_transactions = 5
		
		self.difficulty = 4
		
		self.__chain.append(Block(0,"0",[],1))
		
	def isValidNonce(self,nonce,prev_nonce=None):
		if prev_nonce is None:
			prev_nonce = self.__chain[-1].nonce
		return hashlib.sha256(f'{prev_nonce}{nonce}'.encode()).hexdigest()[:self.difficulty] == "0"*self.difficulty
	
	def newBlock(self,nonce,miner):
		if self.isValidNonce(nonce) and self.__freeblocks.count([nonce,self.difficulty])==0:
			self.__freeblocks.append([nonce,self.difficulty])
			return True
		return False
		
	def newTransaction(self,transaction):
		self.__transactions.append(transaction)
		
	def getChain(self):
		return self.__chain
		
	def update(self):
		blocks_count = 0
		while len(self.__transactions) >= self.__max_transactions and len(self.__freeblocks) > 0:
			free_block = self.__freeblocks.popleft()
			last_block = self.__chain[-1]
			transactions = []
			for i in range(self.__max_transactions):
				transactions.append(self.__transactions.popleft())
			block = Block(last_block.index + 1,last_block.hash,transactions,free_block[0])
			self.__chain.append(block)
			blocks_count+=1
		return blocks_count
		
	def isValid(self):
		prev_block = self.__chain[0]
		for block in self.__chain[1:]:
			if Block.calculateHash(block) != block.hash:
				return False
			if block.prev_hash != prev_block.hash:
				return False
			if not self.isValidNonce(block.nonce,prev_block.nonce):
				return False
			prev_block = block
		return True
		
	def __repr__(self):
		 return json.dumps({'blocks' : self.__chain}, default=lambda o: o.__dict__, sort_keys=True, indent=4)
	
	@property
	def __dict__(self):
		return {
				'blocks' : self.__chain,
				'transactions' : list(self.__transactions),
				'free_blocks' : list(self.__freeblocks), 
				'max_block_transactions_size' : self.__max_transactions,
				'difficulty' : self.difficulty
				}
				
	@staticmethod
	def from_dict(dict):
		blockchain = BlockChain()
		for transaction in dict['transactions']:
			blockchain.__transactions.append(Transaction.from_dict(transaction))
		blockchain.__chain = []
		for block in dict['blocks']:
			blockchain.__chain .append(Block.from_dict(block))
		for free_block in dict['free_blocks']:
			blockchain.__freeblocks.append(free_block)
		blockchain.__max_transactions = dict['max_block_transactions_size']
		blockchain.difficulty = dict['difficulty']
		return blockchain
							
if __name__ == "__main__":
	blockchain = BlockChain()
	print(json.dumps({'chain':blockchain},default=lambda o: o.__dict__,indent=4))