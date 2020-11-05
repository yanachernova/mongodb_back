import os
from datetime import timedelta

# settings.py
from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DEBUG = True
ENV = 'development'

 # JWT configuration
JWT_SECRET_KEY = 'secret'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

# Files configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
UPLOAD_FOLDER = UPLOAD_FOLDER

# Mail configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

