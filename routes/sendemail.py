import os
from flask import Blueprint, request, jsonify
from libs.functions import sendMail
route_sendemail = Blueprint('route_sendemail', __name__)
@route_sendemail.route('/sendemail', methods=['POST'])
def sendemail():
    subject = '..::GoDrunk MESSAGE::..'
    
    sendMail(subject, "Yana", os.getenv('MAIL_USERNAME'), ["fineukraine94@gmail.com", "yana.chernova94@gmail.com"], '<div><p>Hello</p></div>')
    return jsonify({"success": "Your email sended"}), 200


""" to_email = os.getenv('MAIL_NAME')
    name = request.json.get('name', None)
    from_email = request.json.get('from_email', None)
    phone = request.json.get('phone', None)
    message = request.json.get('message', None)
    company = request.json.get('company', None)
    if not name:
        return jsonify({"error": "Nombre es obligatorio"}), 422
    if not from_email:
        return jsonify({"error": "Email es obligatorio"}), 422
    if not phone:
        return jsonify({"error": "Teléfono es obligatorio"}), 422
    if not message:
        return jsonify({"error": "Mensaje es obligatorio"}), 422
    if not company:
        return jsonify({"error": "Empresa es obligatorio"}), 422 """