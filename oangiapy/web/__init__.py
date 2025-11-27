from flask import make_response, jsonify

class FlaskAdapter:
    def __init__(self, request):
        # Adapt input
        self.data = self._extract_data(request)
        self.headers = self._extract_headers(request)

    def _extract_data(self, request):
        if request.is_json:
            return request.get_json()
        if request.form:
            return dict(request.form)
        if request.args:
            return dict(request.args)
        return {}

    def _extract_headers(self, request):
        return dict(request.headers)

    def get_client_ip(request):
        """
        Get client IP based on priority:
        1. X-Real-IP
        2. X-Forwarded-For (first IP)
        3. remote_addr
        """
        ip = request.headers.get("X-Real-IP")
        if ip:
            return ip.strip()
    
        xff = request.headers.get("X-Forwarded-For")
        if xff:
            return xff.split(",")[0].strip()
    
        return request.remote_addr

    def data(self):
        return self.data

    def headers(self):
        return self.headers

    @staticmethod
    def adapt_response(payload, status=200, extra_headers=None):
        """
        Adapt core output into a Flask response.
        Does NOT call core logic.
        """
        resp = make_response(jsonify(payload), status)
        # Add CORS by default
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"

        # Add any extra headers if provided
        if extra_headers:
            for k, v in extra_headers.items():
                resp.headers[k] = v

        return resp
