from flask import Flask
from flask import request
from flask import send_file
from flask_restplus import fields
from flask_restplus import reqparse, Api, Resource
import pickle
import numpy as np
import pymongo
from model import NLPModel
import requests
import operator
from pymongo import MongoClient
from flask import render_template, redirect, url_for, request, session
import config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config)

api = Api(app,
          default="Comment",  # Default namespace
          title="Movie Comment Emotion Analysis",  # Documentation Title
          description="Given a movie comment by customer, then return the emotion of this comment based on machine learning")  # Documentation Description

connection = pymongo.MongoClient('ds255282.mlab.com', 55282)
db = connection['assignment']
db.authenticate('z5145696', 'Magic8484')
account = db['account']


@app.route('/handle_data', methods = ['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        return render_template("search.html")
    if request.method == 'GET':
        query = request.args.get('content')

        model = NLPModel()

        clf_path = 'lib/models/SentimentClassifier.pkl'
        with open(clf_path, 'rb') as f:
            model.clf = pickle.load(f)

        vec_path = 'lib/models/TFIDFVectorizer.pkl'
        with open(vec_path, 'rb') as f:
            model.vectorizer = pickle.load(f)

        user_query = query
        uq_vectorized = model.vectorizer_transform(np.array([user_query]))
        prediction = model.predict(uq_vectorized)
    # print(prediction)
        pred_proba = model.predict_proba(uq_vectorized)

        confidence = round(pred_proba[0], 3)
        print(prediction,confidence)

        if prediction == 0:
            filename = 'cry.jpg'
            return send_file(filename, mimetype='image/jpg')
        else:
            filename = 'smile.jpg'
            return send_file(filename, mimetype='image/jpg')



@app.route('/handle_login', methods = ['POST', 'GET'])
def handle_login():
    if request.method == 'POST':
        return render_template("login.html")
    if request.method == 'GET':
        user = request.args.get('Username')
        password = request.args.get('Password')
        print(account)
        for i in account.find():
            if user in i['username'] and password in i['password']:
                return render_template("search.html")
            else:
                continue
        return u'password or username error'


@app.route('/handle_register', methods = ['POST', 'GET'])
def handle_register():
    mydict = {}
    if request.method == 'POST':
        return render_template("intro.html")
    if request.method == 'GET':
        user = request.args.get('Username')
        password = request.args.get('Password')
        # user = request.args.get('Username')
        # password = request.args.get('Password')
        # return u'regester success'
        mydict = {"username": user, "password": password}
        account.insert_one(mydict)
        for i in account.find():
            if user in i['username'] and password == i['password']:
                return u'password or username already exist'
            else:
                continue
        return render_template('login.html')




if __name__ == '__main__':
    app.run(host = 'localhost',port = 5000)
