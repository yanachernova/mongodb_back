import os
import ssl
from flask import Blueprint, jsonify, request, current_app, render_template
from flask_pymongo import pymongo, ObjectId
from flask_jwt_extended import jwt_required

#Database connection information
CONNECTION_STRING = f"mongodb+srv://fineukraine:{os.getenv('MONGO_DB_PASSWORD')}@cluster0.hcua8.mongodb.net/godrunk?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
#Database Name
db = client.get_database('godrunk')
table = db.data

route_datas = Blueprint('route_datas', __name__)
@route_datas.route('/datas', methods=['GET'])
@jwt_required
def getData():
    data=[]
    for doc in table.find():
        data.append({
            '_id': str(ObjectId(doc['_id'])),
            'subject': doc['subject'],
            'user_id': doc['user_id']
        })
    return jsonify(data), 200

@route_datas.route('/datas', methods=['POST'])
@jwt_required
def createData():
    id = table.insert({
        'subject': request.json['subject'],
        'user_id': request.json['user_id']
    })
    return jsonify(str(ObjectId(id))), 200

@route_datas.route('/data/<id>', methods=['DELETE'])
@jwt_required
def deleteData(id=None):
    for doc in table.find():
        if doc['user_id'] == id:
            table.delete_one({'_id': ObjectId(doc['_id'])})
    return jsonify({'success': 'Deleted!'}),200


