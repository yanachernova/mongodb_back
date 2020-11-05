from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import(
    JWTManager, get_jwt_identity
)
from flask_mail import Mail

from routes.user import route_users
from routes.data import route_datas
from routes.email import route_emails
from routes.sendemail import route_sendemail

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config.from_pyfile('settings.py')

mail = Mail(app)
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def flask_mongo_db():
    return render_template('index.html')

app.register_blueprint(route_users)
app.register_blueprint(route_datas)
app.register_blueprint(route_emails)
app.register_blueprint(route_sendemail)
if __name__ == '__main__':
    app.run(port=8000)