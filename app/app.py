from flask import Flask,request,json,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///user.db"
db=SQLAlchemy(app)

class User(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(200),nullable=False)
    lastname=db.Column(db.String(200))
    email=db.Column(db.Text,nullable=False)
    password=db.Column(db.Text,nullable=False)
    datetime=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.email} - {self.password}"

""" 
@app.route("/app",methods=['GET'])
def hello_world():
    user=User(firstname="Nischal" ,lastname="Chaudhary", email="bac@h", password="ABc")
    db.session.add(user)
    db.session.commit()
    alluser=User.query.all()
    print(alluser)
    return{'name':'Hello, World2!'}

@app.route("/show")
def show():
    alluser=User.query.all()
    print(alluser)
    return "show page"

@app.route("/create2/<string:email> <string:pas>")
def create2(email,pas):
    email=email
    user=User.query.filter_by(email=email).first()
    if(user is None):
        new_user=User(firstname="hello" ,lastname="new", email=email, password=pas)
        db.session.add(new_user)
        db.session.commit()
        return {'201':'user added successfully'}
    
    elif(user.password==pas):
        return {'great':'autuentication done'}
    
    else:
        return {'wrong':'wrong username or password'}
    




@app.route("/delete/<string:email>")
def delete(email):
    user=User.query.filter_by(email=email).first()
    if(user is None):
        print("hello")
    else:
        print(type(user))
        print(user.password)
        db.session.delete(user)
        db.session.commit()

    
    return "page"

 """
 
@app.route("/app/create",methods=['POST'])
def login():
    rquest_data=json.loads(request.data)
    email=rquest_data[email]
    user=User.query.filter_by(email=email).first()
    if(user is None):
        new_user=User(firstname=rquest_data[firstname] ,lastname=rquest_data[lastname], email=rquest_data[email], password=rquest_data[password])
        db.session.add(new_user)
        db.session.commit()
        return {'201':'user added successfully'}
    
    elif(user.password==rquest_data[password]):
        return {'great':'autuentication done'}
    
    else:
        return {'wrong':'wrong username or password'}
    


    


if __name__ == "__main__":
    app.run(debug=True)
