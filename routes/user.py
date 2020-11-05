import os
import ssl
from flask import Blueprint, jsonify, request, current_app, render_template
from flask_bcrypt import Bcrypt
from flask_pymongo import pymongo, ObjectId
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

bcrypt = Bcrypt()

#Database connection information
CONNECTION_STRING = f"mongodb+srv://fineukraine:{os.getenv('MONGO_DB_PASSWORD')}@cluster0.hcua8.mongodb.net/godrunk?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
#Database Name
db = client.get_database('godrunk')
table = db.user



route_users = Blueprint('route_users', __name__)

@route_users.route('/register', methods=['POST'])
def registerUser():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    hashed = bcrypt.generate_password_hash(password)
    if not name:
        return jsonify({'error': 'Name is required'}), 422
    if not email:
        return jsonify({'error': 'Email is required'}), 422
    if not password:
        return jsonify({'error': 'Password is required'}), 422

    id = table.insert({
        'name': name,
        'email': email,
        'password': hashed
    })
    return jsonify(str(ObjectId(id))), 200
    
@route_users.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    if not email:
        return jsonify({'error': 'Email is required'}), 422
    if not password:
        return jsonify({'error': 'Password is required'}), 422
    user = table.find_one({'email': email})
    if user:
        if bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity={'name': user['name'], 'email': user['email']})

            return jsonify({
                "access_token": access_token,
                "user": {
                '_id': str(ObjectId(user['_id'])),
                'name': user['name'],
                'email': user['email']
                }
            }), 200
        else: 
            return jsonify({"error": "Password is incorrect"}), 401  
    else:
        return jsonify({"error": "Email is not register"}), 401

@route_users.route('/users', methods=['GET'])
@jwt_required
def getUsers():
    users=[]
    for doc in table.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email']
        })
    return jsonify(users), 200

@route_users.route('/user/<id>', methods=['GET'])
@jwt_required
def getUser(id):
    user = table.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
    })

@route_users.route('/user/<id>', methods=['PUT'])
@jwt_required
def updateUser(id):
    table.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password'],
    }})
    return jsonify({'success':'Updated!'}),200

@route_users.route('/user/<id>', methods=['DELETE'])
@jwt_required
def deleteUser(id):
    table.delete_one({'_id': ObjectId(id)})
    return jsonify({'success': 'Deleted!'}),200






