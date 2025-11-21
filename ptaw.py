from flask import Flask, request, jsonify
from oangiapy.readability import handle_request, cors

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    data, status = handle_request(request)
    return cors(jsonify(data), status)

if __name__ == '__main__':
    app.run()
