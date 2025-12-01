from oangiapy.agent52 import run
# pythonanywhere
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    return run(request)

if __name__ == '__main__':
    app.run()

# gcloud
import functions_framework

@functions_framework.http
def hello_http(request):
    return run(request)
