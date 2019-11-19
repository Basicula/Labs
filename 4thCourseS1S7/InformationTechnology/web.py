import requests
import os
import json
from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient("mongodb://Basicula:5basicula5@testcluster-shard-00-00-zwdzb.gcp.mongodb.net:27017,testcluster-shard-00-01-zwdzb.gcp.mongodb.net:27017,testcluster-shard-00-02-zwdzb.gcp.mongodb.net:27017/test?ssl=true&replicaSet=TestCluster-shard-0&authSource=admin&retryWrites=true&w=majority")

def load_db(db_name):
    for root, directories, files in os.walk('server'):
        for filename in files:
            if '.json' in filename and db_name == filename.split('.')[0]:
                with open("server/"+filename, 'r') as file:
                    data = json.load(file)
                    return False,data
                    
    mongo_db = client.list_database_names()[:-2]
    if db_name in mongo_db:
        tables = list(client[db_name]["tables"].find())
        for table in tables:
            table.pop("_id")
        if len(tables) == 1 and tables[0]["name"] =="" and len(tables[0]["columns"]) == 0 and len(tables[0]["rows"]) == 0:
            tables = []
        return True,{"name" : db_name, "tables": tables}
                    
def save_db(db,filename="",mongo=False):
    if not mongo:
        if filename=="":
            filename = db["name"]
        with open("server/"+filename+".json", 'w') as file:
            json.dump(db,file)
    else:
        tables = client[db["name"]]["tables"]
        tables.remove()
        tables.insert(db["tables"])

app = Flask(__name__)

@app.route('/', methods=['GET'])
def start_page():
    return render_template('index.html')
    
@app.route('/databases',methods=['GET','POST'])
def databases():
    if request.method == "GET":
        result = {}
        names = []        
        for root, directories, files in os.walk('server'):
            for file in files:
                if '.json' in file:
                    names.append(file.split('.')[0])
        result["local"] = names
        result["mongo"] = client.list_database_names()[:-2]
        response = {"result" : result,"status" : "OK"}
        return response
    elif request.method == "POST":
        mongo = request.form["mongo"]
        db_name = request.form["db_name"]
        if mongo:
            newdb = client[db_name]
            tables = newdb["tables"]
            empty_table = {"name" : "", "columns": [], "rows":[]}
            tables.insert_one(empty_table)
        else:
            data = {}
            data["name"] = db_name
            data["tables"] = []
            save_db(data)
        return {"status" : "OK", "message" : "Database " + db_name + " created"}
        
@app.route('/databases/<db_name>',methods=['DELETE'])
def delete_database(db_name):
    os.remove('server/'+db_name+'.json')
    return {"status" : "OK", "message" : "Database " + db_name + " removed"}
    
@app.route('/databases/<database>/tables',methods=['GET','POST'])
def tables(database):
    if request.method == "GET":
        tables = []
        mongo, data = load_db(database)
        tables = list(map(lambda x : x["name"],data["tables"]))
        response = {"result" : tables,"status" : "OK"}
        return response
    elif request.method == "POST":
        mongo, data = load_db(database)
        table = {}
        table["name"] = request.form["name"]
        table["columns"] = []
        table["rows"] = []
        types = request.form.getlist("types[]")
        headers = request.form.getlist("headers[]")
        for t,h in zip(types,headers):
            table["columns"].append({"header" : h, "type" : t})
        data["tables"].append(table)
        save_db(data,database,mongo)
        return {"status" : "OK", "message" : "Table " + table["name"] +" added"}
        
@app.route('/databases/<database>/mergetables',methods=['POST'])
def merge_tables(database):
    tables = request.form.getlist("tables[]")
    new_name = request.form["new_name"]
    if new_name == "":
        new_name = "+".join(tables)
    new_table = {}
    new_table["name"] = new_name
    new_table["columns"] = []
    new_table["rows"] = []
    tables_to_merge = []
    mongo, data = load_db(database)
    for i in range(len(data["tables"])):
        table = data["tables"][i]
        if table["name"] in tables:
            tables.remove(table["name"])
            tables_to_merge.append(table)
    row_length = 0
    row_cnt = 0
    for table in tables_to_merge:
        row_length += len(table["columns"])
        row_cnt += len(table["rows"])
        for column in table["columns"]:
            new_table["columns"].append(column)
    for i in range(row_cnt):
        row = []
        for j in range(row_length):
            cell = {}
            cell["data"] = ""
            cell["type"] = new_table["columns"][j]["type"]
            row.append(cell)
        new_table["rows"].append(row)
    x = 0
    y = 0
    for table in tables_to_merge:
        for i,row in enumerate(table["rows"]):
            for j,cell in enumerate(row):
                new_table["rows"][i+x][j+y] = cell
        x+=len(table["rows"])
        y+=len(table["columns"])
    data["tables"].append(new_table)
    save_db(data,database,mongo)    
    return {"status" : "OK", "message" : "Merged successful"}
    
    
@app.route('/databases/<database>/tables/<tablename>',methods=['GET','DELETE'])
def table(database,tablename):
    if request.method == "GET":
        response = {"result" : None,"status" : "OK"}
        mongo, data = load_db(database)
        for table in data["tables"]:
            if table["name"] == tablename:
                response["result"] = table
        return response
    elif request.method == "DELETE":
        response = {"status" : "OK", "message" : "Table " + tablename + " removed"}
        mongo, data = load_db(database)
        for table in data["tables"]:
            if table["name"] == tablename:
                data["tables"].remove(table)
        save_db(data,database,mongo)
        return response
    
@app.route('/databases/<database>/tables/<tablename>/rows',methods=['DELETE'])
def delete_row(database,tablename):
    mongo, data = load_db(database)
    for i,table in enumerate(data["tables"]):
        if table["name"] == tablename:
            data["tables"][i]["rows"].remove(data["tables"][i]["rows"][int(request.form["index"])])
    save_db(data,database,mongo)
    response = {"status":"OK"}
    return response
    
@app.route('/databases/<database>/tables/<tablename>/row',methods=['POST'])
def add_row(database,tablename):
    mongo, data = load_db(database)
    table = None
    for i,t in enumerate(data["tables"]):
        if t["name"] == tablename:
            table = t        
    row = []
    for celldata,col in zip(request.form.getlist("cells[]"),table["columns"]):
        cell = {}
        cell["data"] = celldata
        cell["type"] = col["type"]
        row.append(cell)
    table["rows"].append(row)
    save_db(data,database, mongo)
    return {"status" : "OK", "message" : "Row added"}
    
if __name__ == "__main__":
    app.run(debug=True,port=5000)