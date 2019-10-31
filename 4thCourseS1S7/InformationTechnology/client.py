import socket
import json

from database import *

CODE = 'utf-8'
BUFFER_SIZE = 8192

class Client:
    def __init__(self,host='127.0.0.1',port=65432):
        self.host = host
        self.port = port
        
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host,self.port))
        except:
            print("server down")

    def post(self,data):
        try:
            self.socket.send(data.encode(CODE))
        except:
            print("server is dead")
        
    def get(self):
        try:
            data = self.socket.recv(BUFFER_SIZE).decode(CODE)
            return data
        except:
            print("connection lost")
            
    def getAllDataBases(self):
        try:
            self.socket.send('all names'.encode(CODE))
        except:
            print("server is dead")
        try:
            data = json.loads(self.socket.recv(BUFFER_SIZE).decode(CODE))
            return data['databases']
        except:
            print("connection lost")
            
    def getDataBaseByName(self,name):
        try:
            self.socket.send(json.dumps({'database by name' : name}).encode(CODE))
        except:
            print("server is dead")
            
        database = DataBase.fromDict(json.loads(self.socket.recv(BUFFER_SIZE).decode(CODE)))
        return database
        
    def mergeTables(self,db,names):
        try:
            self.socket.send(json.dumps({'merge tables' : names , 'database' : db}).encode(CODE))
        except:
            print("server is dead")
            
    def deleteTables(self,db,names):
        try:
            self.socket.send(json.dumps({'delete tables' : names , 'database' : db}).encode(CODE))
        except:
            print("server is dead")
            
    def saveDataBase(self,db):
        try:
            self.socket.send(json.dumps({'save database' : json.dumps(db,default=lambda o: o.__dict__)}).encode(CODE))
        except:
            print("server is dead")
            
    def deleteDataBases(self,names):
        try:
            self.socket.send(json.dumps({'delete databases' : names}).encode(CODE))
        except:
            print("server is dead")
            
    def updateTable(self,database,table,new_table):
        try:
            self.socket.send(json.dumps({'update table' : {'database':database,'table':table,'new_table':json.dumps(new_table,default=lambda o: o.__dict__)}}).encode(CODE))
        except:
            print("server is dead")

if __name__ == "__main__":
    client = Client()
    client.connect()