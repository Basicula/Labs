from blockchain import BlockChain
from transaction import Transaction,TransactionType
from collections import deque
import json
import hashlib
import threading
import random
import string
import time 

class User:
	def __init__(self,name,balance = 0):
		self.name = name
		self.balance = balance
		
	@property
	def __dict__(self):
		return {"username" : self.name, "balance" : self.balance}
		
	@staticmethod
	def from_dict(dict):
		return User(dict['username'],dict['balance'])

class Server:
	def __init__(self,server_name="System"):
		self.server_name = server_name
		self.__miners = deque()
		self.__blockchain = BlockChain()
		self.__users = [User(self.server_name,float("inf"))]
				
	@staticmethod
	def from_dict(dict):
		server = Server(dict['server_name'])
		server.__blockchain = BlockChain.from_dict(dict['chain'])
		if not server.__blockchain.isValid():
			raise Exception("Blockchain isn't valid")
		server.__users = []
		for user in dict['users']:
			server.__users.append(User.from_dict(user))
		return server
		
	def saveServerState(self):
		self.update()
		with open("server.json", 'w') as outfile:
			json.dump({	'server_name' : self.server_name,
						'chain' : self.__blockchain, 
						'users' : self.__users
						}, outfile, default=lambda o: o.__dict__, indent=4)
			
	@property
	def userCount(self):
		return len(self.__users) - 1
	
	def isExistUser(self,username):
		for user in self.__users:
			if user.name == username:
				return True
		return False
		
	def newUser(self,username):
		if not self.isExistUser(username):
			self.__users.append(User(username,0))
			print(f"New user {username} were created")
			return True
		print(f"{username} already exist")
		return False
	
	@staticmethod
	def findNextNonce(prev_nonce,difficulty,nonce=0):
		while hashlib.sha256(f'{prev_nonce}{nonce}'.encode()).hexdigest()[:difficulty] != "0"*difficulty:
			nonce+=1
		return nonce
		
	def mineBlock(self,username):
		last_nonce = self.__blockchain.getChain()[-1].nonce
		nonce = self.findNextNonce(last_nonce,self.__blockchain.difficulty)
		if self.__blockchain.newBlock(nonce,username):
			self.__blockchain.newTransaction(Transaction(TransactionType.REWARD,self.server_name,username,self.__blockchain.difficulty/10))
			self.update()
			return True
		return False
	
	def mine(self,username=None):
		if username:
			self.__miners.append(username)
		if len(self.__miners) == 0:
			return
		miner = self.__miners.popleft()
		while self.mineBlock(miner):
			print(f"{miner} mined new block!")
			miner = None
			if len(self.__miners) > 0:
				miner = self.__miners.popleft()
			else:
				break
		if miner is not None:
			self.__miners.appendleft(miner)
		
	def sendFromTo(self,sender_name,recipient_name,amount,message=""):
		sender = self.findUserByName(sender_name)
		if sender.balance >= amount:
			self.__blockchain.newTransaction(Transaction(TransactionType.FROMTO,sender_name,recipient_name,amount,message))
			self.update()
			print(f"{sender_name} sent {recipient_name} {amount} with message \"{message}\"")
			return True
		print(f"{sender_name} tried to send {recipient_name} {amount} with message \"{message}\"")
		return False
			
	def buy(self,recipient_name,amount):
		self.__blockchain.newTransaction(Transaction(TransactionType.BUY,self.server_name,recipient_name,amount))
		self.update()
		print(f"{recipient_name} bought {amount}")
		
	def sell(self,sender_name,amount):
		sender = self.findUserByName(sender_name)
		if sender.balance >= amount:
			self.__blockchain.newTransaction(Transaction(TransactionType.SELL,sender_name,self.server_name,amount))
			self.update()
			print(f"{sender_name} sold {amount}")
			return True
		print(f"{sender_name} tried to sell {amount}")
		return False
		
	def findUserByName(self,username):
		for user in self.__users:
			if user.name == username:
				return user
		
	def getRandomUser(self):
		return random.choice(self.__users[1:]).name
		
	def updateBalance(self,username,delta):
		user = self.findUserByName(username)
		user.balance += delta
	
	def update(self):
		blocks_count = self.__blockchain.update()
		if blocks_count == 0:
			return
		blocks = self.__blockchain.getChain()[-blocks_count:]
		for block in blocks:
			for transaction in block.transactions:
				if transaction.type == TransactionType.REWARD:
					self.updateBalance(transaction.recipient,transaction.amount)
				elif transaction.type == TransactionType.FROMTO:
					self.updateBalance(transaction.recipient,transaction.amount)
					self.updateBalance(transaction.sender,-transaction.amount)
				elif transaction.type == TransactionType.BUY:
					self.updateBalance(transaction.recipient,transaction.amount)
				elif transaction.type == TransactionType.SELL:
					self.updateBalance(transaction.sender,-transaction.amount)

def generateRandomString(max_length,characters):
	length = random.randint(2,max_length)
	res = ""
	for i in range(length):
		res += random.choice(characters)
	return res
	
def isNumber(number):
	try:
		int(number)
		return True
	except:
		return False

def simulate():
	data = None
	loadfile = "server.json"
	try:
		with open(loadfile, "r") as read_file:
			data = json.load(read_file)
		server = Server.from_dict(data)
	except Exception as error:
		print(error)
		print("Failed to load server")
		return
	
	max_name_length = 20
	max_message_length = 1000
	name_characters = string.ascii_letters + "0123456789"
	message_characters = name_characters + ", . / ' ; : [ ] { } ( ) | \\ ? > < & ^ % $ # @ ! - _ + = № ' ' \" "
	max_buy = 1000000
	iterations = 0	
	while True:
		mode = -1
		if iterations == 0:
			response = input(
		"What to do?\n\
		simulate <number> - auto process a little\n\
		info <username> -  display info about user\n\
		create <username> - create special user\n\
		mine <username> - try mine for this user\n\
		send <sender> <recipient> <amount> <message> - try send\n\
		buy <username> <amount> - buy\n\
		sell <username> <amount> - sell\n\
		0 - create new user\n\
		1 - try to mine block\n\
		q - quit and save process\n\
		qq - take a French leave\n")
			if response[:8] == "simulate":
				try:
					iterations = int(response[9:])
				except:
					print("Incorect iterations number try again")
			elif response[:4] == "info":
				user_name = response[5:]
				if server.isExistUser(user_name):
					user = server.findUserByName(user_name)
					print(f"{user.__dict__}")
				else:
					print(f"{user_name} doesn't exist")
			elif response[:6] == "create":
				server.newUser(response[7:])
			elif response[:4] == "mine":
				if server.isExistUser(response[5:]):
					if server.mineBlock(response[5:]):
						print("Block mined!")
					else:
						print("Mine failed :(")
				else:
					print("User doesn't exist")
			elif response[:4] == "send":
				data = response[5:].split()
				if not server.isExistUser(data[0]):
					print(f"User {data[0]} doesn't exist")
				elif not server.isExistUser(data[1]):
					print(f"User {data[1]} doesn't exist")
				elif not isNumber(data[2]):
					print(f"Bad amount value: {data[2]}")
				data.append("")
				server.sendFromTo(data[0],data[1],int(data[2]),data[3])
			elif response[:3] == "buy":
				user,amount = response[4:].split()
				if not server.isExistUser(user):
					print(f"User {data[0]} doesn't exist")
				elif not isNumber(amount):
					print(f"Bad amount value: {amount}")
				server.buy(user,int(amount))
			elif response[:4] == "sell":
				user,amount = response[4:].split()
				if not server.isExistUser(user):
					print(f"User {data[0]} doesn't exist")
				elif not isNumber(amount):
					print(f"Bad amount value: {amount}")
				server.sell(user,int(amount))
			elif response == "0":
				mode = 0
			elif response == "1":
				mode = 1
			elif response == "q":
				break
			elif response == "qq":
				return
			else:
				print("Incorect input try again")
				continue
				
		if iterations == 0:
			continue
		if mode == -1:
			mode = random.randint(0,5)
		if mode > 0 and server.userCount < 2:
			continue
		if mode == 0:
			new_name = generateRandomString(max_name_length,name_characters)
			server.newUser(new_name)
		elif mode == 1:
			new_miner = random.randint(0,2)
			if new_miner == 1:
				server.mine(server.getRandomUser())
			else:
				server.mine()
		elif mode == 2:
			user = server.getRandomUser()
			amount = random.uniform(0,max_buy)
			server.buy(user,amount)
		elif mode == 3:
			user = server.getRandomUser()
			amount = random.uniform(0,max_buy)
			server.sell(user,amount)
		elif mode == 4:
			sender = server.getRandomUser()
			recipient = server.getRandomUser()
			while sender == recipient:	
				recipient = server.getRandomUser()
			amount = random.uniform(0,max_buy)
			message = generateRandomString(max_message_length,message_characters)
			server.sendFromTo(sender,recipient,amount,message)
		iterations-=1
	
	server.saveServerState()
	print("Server saved")

if __name__ == "__main__":
	simulate()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	