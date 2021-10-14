'''
Stub for MIBS system
'''
from flask import Flask, request

app = Flask(__name__)

'''
Return message for GET request
'''
@app.route('/mibs/hello',methods=['POST','GET'])
def info():
  if request.method == 'GET':
    return 'Hello from MIBS'
  else:
    return 'No Get'


