from flask import Flask, request
from oangiapy.readability import analyze
from oangiapy.web import FlaskAdapter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    adapter = FlaskAdapter(request)
    # Handle OPTIONS pre-flight or invalid origin
    if adapter.preflight():
        return adapter.respPreflight()
    # Pass adapted request to core
    result, status = analyze(adapter)
    # Convert core output to Flask response
    return adapter.resp(result, status)

if __name__ == '__main__':
    app.run()
