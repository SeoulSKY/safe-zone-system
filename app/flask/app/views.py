from app import app
import os

@app.route("/cms/hello", methods=['POST','GET'])
def index():
    return "Hello from CMS"