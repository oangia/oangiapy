from flask import make_response, jsonify

class FlaskAdapter:
    ALLOWED_ORIGIN = "https://agent52.web.app"

    def __init__(self, request):
        self._request = request
        self._headers = dict(request.headers)
        self._ip = self._extract_ip(request)

        # Handle OPTIONS pre-flight
        if request.method == "OPTIONS":
            self._data = {}
            self._status = 200
            self._preflight = True
        # Check allowed origin
        elif request.headers.get("Origin") != self.ALLOWED_ORIGIN:
            self._data = {"error": "Not found"}
            self._status = 404
            self._preflight = True
        else:
            self._data = self._extract_data(request)
            self._status = 200
            self._preflight = False

    def _extract_data(self, request):
        if request.is_json:
            return request.get_json()
        if request.form:
            return dict(request.form)
        if request.args:
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
        return self._data

    def headers(self):
        return self._headers

    def get_client_ip(self):
        return self._ip

    def preflight(self):
        """Returns True if request was OPTIONS or invalid origin"""
        return getattr(self, "_preflight", False)

    def preflight_status(self):
        return getattr(self, "_status", 200)

    def resp(self, payload, status=200, extra_headers=None):
        resp = make_response(jsonify(payload), status)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        if extra_headers:
            for k, v in extra_headers.items():
                resp.headers[k] = v
        return resp
