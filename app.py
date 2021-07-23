from flask import Flask,render_template,request,redirect
from flask.helpers import url_for
from dotenv import load_dotenv

import os
from pymongo import MongoClient


app=Flask(__name__)

load_dotenv
mongo_uri = os.getenv('MONGO_URI')
cluster = MongoClient(mongo_uri)

db = cluster["Polling_App"]

collection = db["Names"]

@app.route('/',methods=['GET','POST'])
def get_names():
    val=[]
    for x in collection.find({},{"_id" : 0 ,"Name" : 1}):
        y = x["Name"]
        val.append(y)
    print(val)
    return render_template("index.html",val=val)


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/enter-names',methods=["GET","POST"])
def enter_names():
    num = int(request.values.get("num"))
    return render_template("upload.html",num=num)

@app.route('/insert',methods=["GET", "POST"])
def insert():
    desc = request.values.getlist("fname")
    print(desc)
    ran = len(desc)
    print(ran)

    for i in range(0,ran):
        l=desc[i]
        query={"Name": l}
        collection.insert(query)
    # return "Names added Successfully!"
    return redirect(url_for("admin"))

@app.route('/update',methods=["GET","POST"])
def update():
    val = []
    for x in collection.find({},{"_id" : 0 , "Name" : 1}):
        y = x["Name"]
        val.append(y)
    val2 = len(val)
    for i in range(0,val2):
        ln = val[i]
        query = {"Name" : ln}
        newvalues = { "$set": { 'id' : i }}
        collection.update_one(query , newvalues)
    val = []
    for x in collection.find({},{"id" : 1 , "Name" : 1}):
        y = x["Name"]
        val.append(y)
    val2 = []
    for z in collection.find({},{'id' : 1 , "Name " : 1}):
        a = x['id']
        val2.append(a)
    val3 = len(val2)


    return render_template("update.html",val3 = val3 ,val =val)

@app.route('/update-view',methods=["GET","POST"])
def update_view():
    # num1 = int(request.form["num1"])
    num1 = int(request.values.get("num1"))
    # print(num1)
    updt = str(request.values.get("upt"))

    query = {'id' : num1}
    newvalues = { "$set" : {"Name" : updt}}
    collection.update_one(query, newvalues)
    # return redirect(url_for("admin"))
    return redirect(request.referrer)



if __name__ == '__main__':
    app.run(debug=True)