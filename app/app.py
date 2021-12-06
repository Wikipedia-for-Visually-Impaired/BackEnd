from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask import Flask,request,json,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Define a flask app
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




# Model saved with Keras model.save()
MODEL_PATH = 'models/model_resnet.h5'
MODEL_PATH1 = 'models/model_mobilenetfinal.h5'


# Load your trained model
model = load_model(MODEL_PATH)
model.make_predict_function()          # Necessary
print('Model loaded. Start serving...')

model1 = load_model(MODEL_PATH1)
model1.make_predict_function()          # Necessary
print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/

#import tensorflow
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('model.h5')
#print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    print(preds)
    return preds

def model_p(img_path,model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    print(preds)
    return preds

@app.route("/app",methods=['GET'])
def hello_world():
    """
    user=User(firstname="Nischal" ,lastname="Chaudhary", email="bac@h", password="ABc")
    db.session.add(user)
    db.session.commit()
    """
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

 
 
@app.route("/app/create",methods=['POST'])
def login():
    rquest_data=json.loads(request.data)
    print(rquest_data)
    email=rquest_data['email']
    user=User.query.filter_by(email=email).first()

    if(user is None):
        new_user=User(firstname=rquest_data['firstname'] ,lastname=rquest_data['lastname'], email=rquest_data['email'], password=rquest_data['password'])
        db.session.add(new_user)
        db.session.commit()
        print("user created")
        result={'201':'user added successfully'}
        return jsonify(result)
    
    elif user.password == rquest_data['password']:
        print("user great done")
        return {'great':'autuentication done'}
    
    else:
        print("wrong",user.password,rquest_data['password'])
        return {'wrong':'wrong username or password'}

    

def func(img_path):
    return "hello this is working"



@app.route("/app/predict",methods=['GET','POST'])
def predict():
    if request.method=='POST':
        print(request.files['image'])
        img=request.files['image']
        img_path="static/"+img.filename
        img.save(img_path)
        p=func(img_path)
        p2=model_p(img_path,model)
        p3=decode_predictions(p2, top=3)[0]
        print(type(p3[0]))
        p4=p3[0]
        p5=p3[0][1]
        print(decode_predictions(p2, top=3)[0])
        # result={'imge':str(p5)}
        # return jsonify(result)

        p_1=model_p(img_path,model1)
        p3_1=decode_predictions(p_1, top=3)[0]
        print(type(p3_1[0]))
        p4_1=p3_1[0]
        p5_1=p3_1[0][1]
        print(decode_predictions(p_1, top=3)[0])
        result={'imge':str(p5_1),
        'imge2':str(p5)}
        return jsonify(result)


    


if __name__ == "__main__":
    app.run(debug=True)
