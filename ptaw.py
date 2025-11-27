from flask import Flask, request
from oangiapy.readability import analyze
from oangiapy.web import FlaskAdapter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    adapter = FlaskAdapter(request, handler=analyze)
    return adapter.process()

if __name__ == '__main__':
    app.run()
