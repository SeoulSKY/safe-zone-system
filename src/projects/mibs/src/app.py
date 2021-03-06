'''
Stub for MIBS system
'''
from flask import Flask, request
from os import environ as env
from models import db, Message
from src.api.mibs import mibs_blueprint
from services.message_pool_service import MessagePoolingService
from auth_init import auth

db_addr = env.get('DB_ADDR')
db_name = env.get('DB_DATABASE')
db_user = env.get('DB_USER')
db_pass = env.get('DB_PASSWORD')
auth_issuer = env.get('AUTH_ISSUER')
db_uri = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_addr}/{db_name}'

app = Flask(__name__)
app.config.update({
  'SQLALCHEMY_DATABASE_URI': db_uri,
  'SQLALCHEMY_TRACK_MODIFICATIONS': False,

  'AUTH_ISSUER': f'http://{auth_issuer}/auth/realms/safe-zone',
  'AUTH_AUDIENCE': 'account',
  'AUTH_JWKS_URI': 'http://keycloak:8080/auth/realms/safe-zone/protocol/openid-connect/certs',
})

auth.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()
    MessagePoolingService().start()

@app.route('/mibs/hello',methods=['POST','GET'])
@auth.require_token
def info():
    '''
    Return message for GET request
    '''
    if request.method == 'GET':
        return 'Hello from MIBS'
    else:
        return 'No Get'


@app.route('/mibs/db_test',methods=['POST','GET'])
def db_test():
    if request.method == 'GET':
        return f'{Message.query.all()}'
    else:
        return 'No Get'


app.register_blueprint(mibs_blueprint)
