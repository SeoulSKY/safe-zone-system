from flask import Flask, request
from models import db, Message, EmailMessageRecipient

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:passsword@localhost:5432'
db.init_app(app)

@app.route('/mibs/hello',methods=['POST','GET'])
def info():
    if request.method == 'GET':
        return 'Hello from MIBS'
    else:
        return 'No Get'


