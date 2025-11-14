import functions_framework
from oangiapy.web import gcloud
@functions_framework.http
def hello_http(request):
    return gcloud(request)