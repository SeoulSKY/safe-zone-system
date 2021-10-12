from flask import Flask, request
import os
from models import db, Message

app = Flask(__name__)

db_name = os.environ.get('DB_DATABASE')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@postgres/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/mibs/hello',methods=['POST','GET'])
def info():
    if request.method == 'GET':
        return 'Hello from MIBS'
    else:
        return 'No Get'


@app.route('/mibs/db_test',methods=['POST','GET'])
def db_test():
    if request.method == 'GET':
        return f"{Message.query.all()}"
    else:
        return 'No Get'