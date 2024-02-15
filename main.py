import pyrebase
import firebase_admin
from firebase_admin import credentials , firestore
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
app = Flask(__name__)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
config = {
"Firebase Configs"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

db=firestore.client()
def liste():
    docs = db.collection("customers").stream()
    try:
        my_dict = { el.id: el.to_dict() for el in docs }
        
    except:
        pass
    return my_dict
@app.route("/liste")
def kullanicilar():
    return render_template("kullanicilar.html",data=liste())
    
@app.route('/')
def hello():
    
    return render_template("kayit.html")


@app.route("/delete",methods=["POST"])
def silme():
    email=request.form.get("email")
    db.collection("customers").document(email).delete()
    return redirect("/liste")
@app.route('/bakiye',methods=['GET'])
def bakiyeget():
    return render_template("bakiye.html")


@app.route('/bakiye',methods=['POST'])
def bakiye():
    email=request.form.get("email")
    bakiye=request.form.get("bakiye")
    print(bakiye)
    db.collection("customers").document(email).update({"bakiye":bakiye})
    return redirect("/liste")
@app.route('/kayit', methods=['POST'])
def process_json():
    first_name=request.form.get("name")
    last_name=request.form.get("soyad")
    daireNo=request.form.get("daireNo")
    email=request.form.get("email")
    password=request.form.get("password")
    auth.create_user_with_email_and_password(email, password)
    db.collection("customers").document(email).set({"name":first_name,"lastName":last_name,"daireNo":daireNo})

    return redirect("/liste")

if __name__ == "__main__":
    app.run(debug=True)
