import os
import ssl
from flask import Blueprint, jsonify, request, current_app, render_template
from flask_pymongo import pymongo, ObjectId
from flask_jwt_extended import jwt_required
from libs.functions import sendMail

#Database connection information
CONNECTION_STRING = f"mongodb+srv://fineukraine:{os.getenv('MONGO_DB_PASSWORD')}@cluster0.hcua8.mongodb.net/godrunk?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
#Database Name
db = client.get_database('godrunk')
table = db.email
table_data = db.data
table_user = db.user

def sendemail(to_email, subject):
    title = '..::GoDrunk MESSAGE::..'
    name = "Yana"
    from_email = os.getenv('MAIL_USERNAME')
    sendMail(title, name, from_email, to_email, subject)

route_emails = Blueprint('route_emails', __name__)
@route_emails.route('/emails', methods=['GET'])
@jwt_required
def getEmail():
    emails=[]
    for doc in table.find():
        emails.append({
            '_id': str(ObjectId(doc['_id'])),
            'email': doc['email'],
            'active': doc['active'],
            'user_id': doc['user_id']
        })
    return jsonify(emails), 200

@route_emails.route('/emails', methods=['POST'])
@jwt_required
def createEmail():
    id = table.insert({
        'email': request.json['email'],
        'active': request.json['active'],
        'user_id': request.json['user_id']
    })
    return jsonify(str(ObjectId(id))), 200

@route_emails.route('/email/<id>', methods=['DELETE'])
@jwt_required
def deleteEmail(id=None):
    test=[]
    for doc in table.find():
        if doc['user_id'] == id:
            table.delete_one({'_id': ObjectId(doc['_id'])})
    return jsonify(test),200

@route_emails.route('/sendemail/<user_id>', methods=['POST'])
#@jwt_required
def sendEmail(user_id=None):
    subject_user=''
    emails = []
    for doc in table.find():
        if doc['user_id'] == user_id:
            emails.append(doc['email'])

    subjects = []
    for doc_data in table_data.find():
        if doc_data['user_id'] == user_id:
            subjects.append(doc_data['subject'])
    
    sendemail(emails, subjects[0])
            
    return jsonify({'success': 'sended'}),200


