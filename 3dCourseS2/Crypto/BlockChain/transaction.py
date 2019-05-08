import enum

class TransactionType(enum.Enum):
	REWARD 	= 0
	FROMTO 	= 1
	BUY		= 2
	SELL	= 3

class Transaction:
	def __init__(self,type,sender,recipient,amount,message=""):
		self.type = type
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.message = message
		
	def __str__(self):
		if self.type == TransactionType.REWARD:
			return "Reward for " + self.recipient + "'s mining " + str(self.amount)
		elif self.type == TransactionType.FROMTO:
			return sender + " paid " + self.recipient + " " + str(self.amount) + " with message " + message
		elif self.type == TransactionType.BUY:
			return self.recipient + " bought " + str(self.amount)
		elif self.type == TransactionType.SELL:
			return self.sender + " sold " + str(self.amount)
		
if __name__ == "__main__":
	print(Transaction(TransactionType.REWARD,"system","Max",10))
	