"""
Stub for development for CMS
"""
from flask import Flask, request

app = Flask(__name__)

"""
Return message for GET request
"""
@app.route('/cms/hello',methods=['POST','GET'])
def info():
    if request.method == 'GET':
        return 'Hello from CMS'
    else:
        return 'No Get'


