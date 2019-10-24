from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, IntegerField, SubmitField

from client import *
from database import *

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

client = Client()
client.connect()

new_database = None
new_table = None

@app.route("/", methods=['GET','POST'])
def main():
    form = Form(request.form)
    new_table = None
    new_database = None
    
    if request.method == 'POST':
        if request.form['submit_button'] == 'Delete selected databases':
            client.deleteDataBases(request.form.getlist('selected_databases'))
    
    form.databases = client.getAllDataBases()

    print(form.errors)

    return render_template('main.html', form=form)
    
@app.route("/database/<database>", methods=['GET','POST'])
def database(database):
    form = Form(request.form)
    
    if request.method == 'POST':
        if request.form['submit_button'] == "Merge selected tables":
            client.mergeTables(database,request.form.getlist('selected_table'))
        elif request.form['submit_button'] == "Delete selected tables":
            client.deleteTables(database,request.form.getlist('selected_table'))
        elif request.form['submit_button'] == "Back":
            return redirect('/')
        
    form.database = client.getDataBaseByName(database)
    
    return render_template('database.html',form=form)
    
    
@app.route("/newdatabase", methods = ['GET','POST'])
def newDatabase():
    form = Form(request.form)
    global new_database
    if new_database == None:
        new_database = DataBase()
    if request.method == 'POST':
        new_database.name = request.form['name']
        client.saveDataBase(new_database)
        new_database = None
        return redirect('/')
    form.database = new_database
    
    return render_template('newdatabase.html', form=form)
    
@app.route("/newtable", methods = ['GET','POST'])
def newTable():
    form = Form(request.form)
    global new_table
    if new_table == None:
        new_table = Table()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Create':
            new_table.name = request.form['table_name']
            print(json.dumps(new_table,default=lambda o: o.__dict__))
            new_database.addTable(new_table)
            new_table = None
            return redirect('/newdatabase')
        elif request.form['submit_button'] == 'Add column':
            new_table.name = request.form['table_name']
            column = Column(request.form['column_header'],DataType.fromDict(request.form['column_type']))
            if request.form['column_type'] == 'realinvl':
                column.optionalInfo = ['interval',[request.form['bottom'],request.form['top']]]
            new_table.addColumn(column)
    elif request.method == 'GET':
        new_table = Table()
    form.table = new_table
    
    return render_template('newtable.html', form=form)
    
@app.route("/database/<database>/<table>", methods=['GET','POST'])
def table(database,table):
    global new_table
    if new_table == None:
        new_table = client.getDataBaseByName(database).getTable(table)
    if request.method == 'POST':
        if request.form['submit_button'] == 'Back':
            new_table = None
            return redirect(url_for('database',database=database))
        elif request.form['submit_button'] == 'Save':
            for i,row in enumerate(new_table.rows):
                for j,cell in enumerate(row):
                    cell.data = request.form[str(i)+'.'+str(j)]
            client.updateTable(database,table,new_table)
            new_table = None
            return redirect(url_for('database',database=database))
        elif request.form['submit_button'] == 'Add row':
            for i,row in enumerate(new_table.rows):
                for j,cell in enumerate(row):
                    cell.data = request.form[str(i)+'.'+str(j)]
            client.updateTable(database,table,new_table)
            row = []
            for column in new_table.columns:
                cell = Cell()
                cell.type = column.type
                cell.optionalInfo = column.optionalInfo
                row.append(cell)
            new_table.rows.append(row)
            
    form = Form(request.form)
    form.table = new_table
    
    return render_template('table.html',form=form)

if __name__ == "__main__":
    app.run()