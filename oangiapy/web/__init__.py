#from .routes.home import home_bp
#from .routes.api import api_bp
import os
base_dir = os.path.dirname(__file__)
def gcloud(request):
    data = {"message": "Hello, World! Second time"}
    status = 200
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ({"status": 204}, 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}
    
    return (data, status, headers)
def create_app():
   # app = Flask(__name__, template_folder=os.path.join(base_dir, "templates"))
    #CORS(app)
    # register blueprints
    #app.register_blueprint(home_bp)
    #app.register_blueprint(api_bp, url_prefix="/api")
    pass
    #return app
