from flask import make_response, jsonify
routes = {}

def route(action):
    def wrapper(func):
        routes[action] = func
        return func
    return wrapper

def dispatch(request):
    try:
        adapter = FlaskRequestAdapter(request)
        if adapter.preflight():
                return adapter.respPreflight()
        action = adapter.get("action")
    
        if not action:
            return adapter.resp({"error": "Missing action"}, 400)
    
        if action not in routes:
            return adapter.resp({"error": "Unknown action"}, 400)

        result, status = routes[action](adapter)
        return adapter.resp(result, status)
    except Exception as e:
        return adapter.resp({"error": str(e)}, 500)

class FlaskRequestAdapter:
    ALLOWED_ORIGIN = "https://agent52.web.app"

    def __init__(self, request):
        self._request = request
        self._headers = dict(request.headers)
        self._ip = self._extract_ip(request)

        # Always extract request data
        self._data = self._extract_data(request)

        # Preflight or invalid-origin detection
        origin = request.headers.get("Origin")
        self._preflight = request.method == "OPTIONS" or origin != self.ALLOWED_ORIGIN
        if request.method == "OPTIONS":
            self._status = 200
        elif origin != self.ALLOWED_ORIGIN:
            self._status = 404
        else:
            self._status = 200

    def _extract_data(self, request):
        if request.is_json:
            return request.get_json()
        elif request.form:
            return dict(request.form)
        elif request.args:
            return dict(request.args)
        return {}

    def _extract_ip(self, request):
        ip = request.headers.get("X-Real-IP")
        if ip:
            return ip.strip()
        xff = request.headers.get("X-Forwarded-For")
        if xff:
            return xff.split(",")[0].strip()
        return request.remote_addr

    # Adapter interface
    def data(self):
        """Return the request payload only"""
        return self._data

    def get(self, param, default = False):
        return self._data.get(param, default)

    def headers(self):
        return self._headers

    def get_client_ip(self):
        return self._ip

    def preflight(self):
        """True if request is OPTIONS or origin not allowed"""
        return self._preflight

    def preflight_status(self):
        return self._status

    def respPreflight(self):
        """Return proper preflight CORS response"""
        if self._status == 200:
            payload = {"message": "Preflight OK"}
        else:
            payload = {"error": "Not allowed"}
        return self.resp(payload, self._status)

    def resp(self, payload, status=200, extra_headers=None):
        resp = make_response(jsonify(payload), status)
        resp.headers["Access-Control-Allow-Origin"] = self.ALLOWED_ORIGIN
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        if extra_headers:
            for k, v in extra_headers.items():
                resp.headers[k] = v
        return resp
