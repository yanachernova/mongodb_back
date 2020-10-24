import os
import ssl
from flask import Blueprint, jsonify, request, current_app, render_template
from flask_pymongo import pymongo, ObjectId

#Database connection information
CONNECTION_STRING = f"mongodb+srv://fineukraine:{os.getenv('MONGO_DB_PASSWORDS')}@cluster0.hcua8.mongodb.net/godrunk?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
#Database Name
db = client.get_database('godrunk',  ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
table = db.user

route_users = Blueprint('route_users', __name__)
@route_users.route('/users', methods=['GET'])
def getUsers():
    users=[]
    for doc in table.find():
        users.append({
            '_id': str(ObjectId(doc['id']))

        })
    return jsonify(users), 200

@route_users.route('/users', methods=['POST'])
def createUser():
    id = table.insert({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify(str(ObjectId(id))), 200

