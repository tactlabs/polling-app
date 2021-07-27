from flask import Flask,render_template,request,redirect,session,jsonify,url_for,flash
from dotenv import load_dotenv

import os
from pymongo import MongoClient


app=Flask(__name__)
app.config['SECRET_KEY'] = '4aad4c8ec9d4fe4f72aab7ff4e82cc58'


load_dotenv
mongo_uri = os.getenv('MONGO_URI')
cluster = MongoClient(mongo_uri)

db = cluster["Polling_App"]

collection = db["Names"]

@app.route('/',methods=['GET','POST'])
def login_page():
    return render_template("login.html")

@app.route('/poll_page',methods=['GET','POST'])
def get_names():
    if "user" in session:
        user = session["user"]
        print(user)
        val=[]
        for x in collection.find({},{"_id" : 0 ,"Name" : 1}):
            y = x["Name"]
            val.append(y)
        print(val)
        return render_template("polling_page.html",val=val)
    else:
        return redirect(url_for("login"))


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

@app.route('/delete-view',methods=["GET","POST"])
def delete_view():
    num2 = int(request.values.get("num2"))

    query = {'id' : num2}
    collection.delete_one(query)
    return redirect(request.referrer)

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        flash("Login Successful")
        return redirect(url_for("get_names"))
    else:
        if "user" in session:
            return redirect(url_for("get_names"))
        return render_template("login.html")

@app.route("/logout",methods=["GET","POST"])
def logout():
    if "user" in session:
        flash("You have been logged out!" , "info")
    session.pop("user",None)
    return redirect(url_for("login"))

@app.route('/vote_data',methods=["GET","POST"])
def vote_data():
    collection = db["Vote"]
    if request.method == "POST":
        if "user" in session:

            user = session["user"]
            print(user)
            poll_option = request.form['poll_option']
            print(poll_option)
            query = {"Email" : user , "Vote" : poll_option}
            if collection.find_one({"Vote": query['Vote'], "Email" : query["Email"]}):
                print("Duplicate value found")
                flash("Duplicate value found!")
                # return redirect(request.referrer)
                # return render_template("polling_page.html",msg = msg)
                
            else:    
                collection.insert_one(query)
                print("No duplicate values!")
                flash("No Duplicate value found! Vote submited successfully")
                

            

        return "Your have successfully  voted!"
    

@app.route('/vote_details',methods=["GET","POST"])
def vote_details():
    collection = db["Vote"]
    details =[]
    for x in collection.find():

        email = x['Email']
        vote  = x['Vote']
         
        result = {
            'Email' : email ,
            'Vote'  : vote  
        }
        details.append(result)
        
    print(details)
    return  render_template("vote_details.html",result = details )

@app.route('/drop',methods=['GET','POST'])
def drop():
    collection = db["Vote"]
    collection.delete_many({})

    return redirect(request.referrer) 



if __name__ == '__main__':
    app.run(debug=True)