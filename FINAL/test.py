import requests
import json
import time
import pymongo
import urllib.request
import datetime
import pprint
import pandas as pd
from collections import defaultdict
import pymongo
from pymongo import MongoClient
from flask import Flask,request,jsonify
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from flask_pymongo import PyMongo

mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % ('Conlin', 'Tcgabcd123', 'ds111492.mlab.com', '11492', 'my-database')
client = MongoClient(mongo_uri)
db = client['my-database']
usr_info_1 = {'usr_info':'abc','pwd':'123'}
post = db.usr_info.insert_one(usr_info_1).inserted_id