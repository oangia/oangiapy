from flask import Flask, request
from oangiapy.readability import handler

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    return handler(request)

if __name__ == '__main__':
    app.run()
