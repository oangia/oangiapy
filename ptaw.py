from flask import Flask, request, jsonify
from oangiapy.readability import handle_request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    result = handle_request(request)
    response = jsonify(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    app.run()
