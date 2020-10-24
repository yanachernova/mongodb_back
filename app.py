from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from routes.user import route_users

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

if __name__ == '__main__':
    app.run(port=8000)