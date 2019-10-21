from flask import Flask, render_template, flash, request, redirect
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

new_database = DataBase()

@app.route("/", methods=['GET'])
def main():
    form = Form(request.form)
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
        
    form.database = client.getDataBaseByName(database)
    
    return render_template('database.html',form=form)
    
    
@app.route("/newdatabase", methods = ['GET','POST'])
def newDatabase():
    form = Form(request.form)
    
    new_database = DataBase()
    
    return render_template('newdatabase.html', form=form)
    
@app.route("/newtable", methods = ['GET','POST'])
def newTable():
    form = Form(request.form)
    if request.method == 'GET':
        form.table = Table()
    elif request.method == 'POST':
        pass
    
    return render_template('newtable.html', form=form)
    
@app.route("/addcolumn/<table>", methods = ['GET','POST'])
def addColumn(table):
    form = Form(request.form)
    print(request.form['column_header'])
    #column = Column(request.form['column_header'],request.form['column_type'])
    #column.optionalInfo
    #table.addColumnData()
    return redirect('/newtable')
    
@app.route("/database/<database>/<table>", methods=['GET'])
def table(database,table):
    form = Form(request.form)
    form.table = client.getDataBaseByName(database).getTable(table)
    for row in form.table.rows:
        for cell in row:
            cell.type = cell.type.__dict__
    
    return render_template('table.html',form=form)

if __name__ == "__main__":
    app.run()