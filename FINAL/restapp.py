
from flask import Flask
from flask import request

from flask_restplus import fields
from flask_restplus import reqparse, Api, Resource
import pickle
import numpy as np
from model import NLPModel

import time
import requests
import operator

from pymongo import MongoClient

from flask import render_template, redirect, url_for, request, session
import config
from functools import wraps
from datetime import datetime
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)
# db = SQLAlchemy(app)
api = Api(app,
          default="Comment",  # Default namespace
          title="Movie Comment Emotion Analysis",  # Documentation Title
          description="Given a movie comment by customer, then return the emotion of this comment based on machine learning")  # Documentation Description

# app.config["MONGO_DBNAME"] = "my-database"
# app.config["MONGO_URI"] = "mongodb://Conlin:Tcgabcd123@ds111492.mlab.com:11492/my-database"

# mongo = PyMongo(app)

# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(20), nullable=False)
#     _password = db.Column(db.String(200), nullable=False)  # 内部使用
#
#     @property
#     def password(self):  # 定义一个外部使用的密码
#         return self._password
#
#     @password.setter  # 设置密码加密
#     def password(self, row_password):
#         self._password = generate_password_hash(row_password)
#
#     def check_password(self, row_password):  # 定义一个反向解密的函数
#         result = check_password_hash(self._password, row_password)
#         return result
#
# # 将数据库查询结果传递到前端页面 Question.query.all(),问答排序
# @app.route('/')
# def index():
#     # context = {
#     #     'questions': Question.query.order_by('-time').all()
#     # }
#     # return render_template('intro.html', **context)
#     return render_template('intro.html')
#
# # 登录页面，用户将登录账号密码提交到数据库，如果数据库中存在该用户的用户名及id，返回首页
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         usern = request.form.get('username')
#         passw = request.form.get('password')
#         user = User.query.filter(User.username == usern).first()
#         if user:
#             if user.check_password(passw):
#                 session['user'] = usern
#                 session['id'] = user.id
#                 session.permanent = True
#                 return redirect(url_for('index'))  # 重定向到首页
#             else:
#                 return u'password error'
#         else:
#             return u'username is not existed'
#
#
# # 定义上下文处理器
# @app.context_processor
# def mycontext():
#     usern = session.get('user')
#     if usern:
#         return {'username': usern}
#     else:
#         return {}
#
#
# # 定义发布前登陆装饰器
# def loginFrist(func):
#     @wraps(func)
#     def wrappers(*args, **kwargs):
#         if session.get('user'):
#             return func(*args, **kwargs)
#         else:
#             return redirect(url_for('login'))
#
#     return wrappers
#
#
# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     # if request.method == 'GET':
#     #     return render_template('register.html')
#     # else:
#     username = request.form.get('username')
#     password = request.form.get('password')
#     user = User.query.filter(User.username == username).first()
#     if user:
#         return 'username existed'
#     else:
#         user = User(username=username, password=password)
#         db.session.add(user)  # 数据库操作
#         db.session.commit()
#         return redirect(url_for('login'))  # 重定向到登录页
#
# # 问答页面
# @app.route('/question', methods=['GET', 'POST'])
# @loginFrist
# def question():
#     if request.method == 'post':
#         return render_template('search.html')
#     else:
#         search = request.form.getvalue('add_submit')
#         # detail = request.form.get('detail')
#         # classify = request.form.get('classify')
#         # author_id = User.query.filter(User.username == session.get('user')).first().id
#         # question = Question(title=title, detail=detail,classify=classify, author_id=author_id)
#         db.session.add(search)
#         db.session.commit()
#     # return redirect(url_for('eval.html'))  # 重定向到登录页
#         return render_template('eval.html', **context)

parser = reqparse.RequestParser()
parser.add_argument('query')
@api.route('/emotions')
class MovieReview(Resource):
    @api.response(404, 'Error')
    @api.response(200, 'OK')
    @api.expect(parser)
    def get(self):
        query = parser.parse_args().get('query')
        # print(query)

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
            e_result = 'Negative'
        else:
            e_result = "Positive"


        return e_result, 200



if __name__ == '__main__':
    # mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % ('Conlin', 'Tcgabcd123', 'ds111492.mlab.com', '11492', 'my-database')
    # client = MongoClient(mongo_uri)
    # db = client['my-database']

    # run the application
    app.run(debug=True)

# movie_Comment_Model = api.model('usr_infp', {
#     'usr_id': fields.String,
#     'pwd': fields.String,
# })
#
# @api.route('/comment_user/<string:id>')
# @api.param('id', 'The collection ID')
# class ID_Class(Resource):
#     @api.response(404, 'Error')
#     @api.response(200, 'OK')
#     @api.doc(description="Get a collection by its ID")
#     def get(self, id):
#         # print(id)
#         flg = 0
#         api_data = mongo.db.comment_user
#         for q in api_data.find():
#             # print(q)
#             # print(id == str(q['_id']))
#             if id == str(q['_id']):
#                 # print(q['_id'])
#                 # print('1111111')
#                 flg = 1
#         # print(flg)
#         if flg:
#             # print(api_data.find_one())
#             q = api_data.find_one({'_id': ObjectId(id)})
#             # print('qqqqqqq',q)
#             output = ({'collection_id': str(q['_id']),
#                        'indicator': q['indicator'],
#                        'indicator_value': q['indicator_value'],
#                        'creation_time': q['creation_time'],
#                        'entries': q['entries']})
#             # print(output)
#             return output, 200
#         else:
#             return "", 404
#
#
# @api.route('/comment_user')
# class All_Class(Resource):
#     @api.expect(indicator_model)
#     @api.response(200, 'OK')
#     @api.response(201, 'Created')
#     @api.response(404, 'Error')
#     @api.doc(description="Add a new indicator data")
#     def post(self):
#
#         flg_1 = 0
#
#         indicator = request.json
#
#         indicator_id = indicator['indicator_id']
#
#         data_list = []
#         for i in range(1, 3):
#             url = ("http://api.worldbank.org/v2/countries/all/indicators/%s?date=2012:2017&format=json&page=%d" % (
#                 indicator_id, i))
#             # print(url)
#             json_val = requests.get(url).json()
#             try:
#                 for line in json_val[1]:
#                     data_list.append(line)
#             except IndexError:
#                 return "", 404
#
#         sorted_data_list = []
#         for line in data_list:
#             sub = {'country': line['country']['value'],
#                    'date': line['date'],
#                    'value': line['value']}
#             sorted_data_list.append(sub)
#
#         api_data = mongo.db.comment_user
#         for q in api_data.find():
#             if indicator_id == q['indicator']:
#                 flg_1 = 1
#
#         #######################################  get data from json   ######################################################
#
#         json_sorted_data = {'indicator': indicator_id,
#                             'indicator_value': 'GDP (current US$)',
#                             'creation_time': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time.time())),
#                             'entries': sorted_data_list}
#         #######################################  input data to mongodb   ######################################################
#         collection = db.comment_user
#         collection.insert_one(json_sorted_data)
#
#         # id = json_sorted_data['indicator']
#
#         # client.close()
#         api_data = mongo.db.comment_user
#         q_1 = api_data.find_one({'indicator': indicator_id})
#         q = json.loads(json_util.dumps(q_1))
#         output = ({'location': '/comment_user/' + str(q['_id']),
#                    'collection_id': str(q['_id']),
#                    'creation_time': q['creation_time'],
#                    'indicator': q['indicator']})
#         if flg_1 == 1:
#             return output, 200
#         elif flg_1 == 0:
#             return output, 201
