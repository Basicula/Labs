import socket
import threading
import os
import json

from database import *

CODE = 'utf-8'

class Server:
    def __init__(self,host = '127.0.0.1', port = 65432):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.path = 'server\\'
        self.getAllFiles()
        
    def start(self):
        print("server starts")
        self.running = True
        
        comm_thread = threading.Thread(target=self.serverCommunocation)
        comm_thread.start()
        
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        while True:
            try:
                conn, addr = self.socket.accept()
            except:
                print("server closed")
                return
            self.addNewUser(conn,addr)
            
    def close(self):
        print("server closing")
        self.running = False
        while len(self.clients)>0:
            self.clients.pop()
        self.socket.close()
            
    def addNewUser(self,conn,addr):
        if not conn:
            return
        for user in self.clients:
            if addr == user[0]:
                return
        print("new user",addr)
        self.clients.append([addr,threading.Thread(target=self.newClient,args=(conn,addr))])
        self.clients[-1][1].start()
            
    def serverCommunocation(self):
        while True:
            config = input()
            if config == 'q':
                self.close()
                return

    def newClient(self,client_socket,address):
        print('Connected by', address)
        while True:
            if not self.running:
                client_socket.send('server closed'.encode(CODE))
                client_socket.close()
                return
            try:
                msg = client_socket.recv(4096).decode(CODE)
            except:
                print("client",address,"disconected")
                client_socket.close()
                return
            if not msg:
                try:
                    client_socket.send(''.encode(CODE))
                except:
                    client_socket.close()
                    return
                continue
            print(address,' >> ', msg)
            if msg == 'all names':
                client_socket.send(json.dumps({'databases' : self.getAvaliableDataBases()}).encode(CODE))
            elif 'save database' in msg:
                request = json.loads(msg)['save database']
                database = DataBase.fromDict(json.loads(request))
                fileName = database.name + '.json'
                self.dbfiles.append(fileName)
                with open(self.path + fileName, 'w') as file:
                    json.dump(database, file, default=lambda o: o.__dict__, indent=4)
            elif 'database by name' in msg:
                fileName = json.loads(msg)['database by name'] + '.json'
                with open(self.path + fileName, 'r') as file:
                    data = json.load(file)
                    client_socket.send(json.dumps(data,indent=4).encode(CODE))
            elif 'merge tables' in msg:
                request = json.loads(msg)
                names = request['merge tables']
                db = request['database'] + '.json'
                with open(self.path + db, 'r') as file:
                    data = json.load(file)
                    database = DataBase.fromDict(data)
                    database.mergeTables(names)
                    with open(self.path + db, 'w') as file:
                        json.dump(database, file, default=lambda o: o.__dict__, indent=4)
            elif 'delete tables' in msg:
                request = json.loads(msg)
                names = request['delete tables']
                db = request['database'] + '.json'
                with open(self.path + db, 'r') as file:
                    data = json.load(file)
                    database = DataBase.fromDict(data)
                    for table in database.tables:
                        if table.name in names:
                            database.tables.remove(table)
                    with open(self.path + db, 'w') as file:
                        json.dump(database, file, default=lambda o: o.__dict__, indent=4)
            elif 'delete databases' in msg:
                request = json.loads(msg)
                names = request['delete databases']
                self.getAllFiles()
                for name in names:
                    fileName = name + '.json'
                    if fileName in self.dbfiles:
                        self.dbfiles.remove(fileName)
                        os.remove(self.path+fileName)
            elif 'update table' in msg:
                request = json.loads(msg)['update table']
                dbfile = request['database'] + '.json'
                table_name = request['table']
                print('table',json.loads(request['new_table']))
                new_table = Table.fromDict(json.loads(request['new_table']))
                with open(self.path + dbfile, 'r') as file:
                    data = json.load(file)
                    database = DataBase.fromDict(data)
                    for i,table in enumerate(database.tables):
                        if table.name in table_name:
                            database.tables[i] = new_table
                            break
                    with open(self.path + dbfile, 'w') as file:
                        json.dump(database, file, default=lambda o: o.__dict__, indent=4)
            else:
                client_socket.send("accept".encode(CODE))
            
    def getAllFiles(self):        
        self.dbfiles = []
        for root, directories, files in os.walk(self.path):
            for file in files:
                if '.json' in file:
                    self.dbfiles.append(file)
                    
    def getAvaliableDataBases(self):
        self.getAllFiles()
        names = []
        for file in self.dbfiles:
            names.append(file.split('.')[0])
        return names

if __name__ == "__main__":
    server = Server()
    server.start()