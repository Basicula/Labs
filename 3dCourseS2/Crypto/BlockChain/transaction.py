import enum
import json

class TransactionType(enum.Enum):
	REWARD 	= 0
	FROMTO 	= 1
	BUY		= 2
	SELL	= 3
	
	@property
	def __dict__(self):
		if self == TransactionType.REWARD:
			return "REWARD"
		elif self == TransactionType.FROMTO:
			return "FROMTO"
		elif self == TransactionType.BUY:
			return "BUY"
		elif self == TransactionType.SELL:
			return "SELL"
	
	@staticmethod
	def from_dict(json):
		if json == "REWARD":
			return TransactionType.REWARD
		elif json == "FROMTO":
			return TransactionType.FROMTO
		elif json == "BUY":
			return TransactionType.BUY
		elif json == "SELL":
			return TransactionType.SELL

class Transaction:
	def __init__(self,type,sender,recipient,amount,message=""):
		self.type = type
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.message = message
	
	@property
	def __dict__(self):
		return {'type' : self.type,
				'sender' : self.sender,
				'recipient' : self.recipient,
				'amount' : self.amount,
				'message' : self.message,
				'description' : self.__repr__()
				}
	@staticmethod
	def from_dict(dict):
		type = TransactionType.from_dict(dict['type'])
		sender = dict['sender']
		recipient = dict['recipient']
		amount = dict['amount']
		message = dict['message']
		return Transaction(type,sender,recipient,amount,message)
	
	def __repr__(self):
		if self.type == TransactionType.REWARD:
			return "Reward for " + self.recipient + "'s mining " + str(self.amount)
		elif self.type == TransactionType.FROMTO:
			return self.sender + " paid " + self.recipient + " " + str(self.amount) + " with message: " + self.message
		elif self.type == TransactionType.BUY:
			return self.recipient + " bought " + str(self.amount)
		elif self.type == TransactionType.SELL:
			return self.sender + " sold " + str(self.amount)
		
if __name__ == "__main__":
	print(json.dumps(Transaction(TransactionType.REWARD,"s","m",10,"asd"),default=lambda o: o.__dict__,indent=4))
		