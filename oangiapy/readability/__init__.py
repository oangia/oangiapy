from oangiapy.readability.ReadabilityEngine import ReadabilityEngine
from oangiapy.web import FlaskAdapter 
from oangiapy.crypto import Crypto
from oangiapy.Youtube import extract_video_data, get_channel_info

def handler(request):
    try:
        adapter = FlaskAdapter(request)
        if adapter.preflight():
            return adapter.respPreflight()
        # Pass adapted request to core
        result, status = analyze(adapter)
        # Convert core output to Flask response
        return adapter.resp(result, status)
    except Exception as e:
        return adapter.resp({"error": str(e)}, 500)

def analyze(adapter):
    data = adapter.data()
    action = data.get("action", "default")
    match action:
        case "yt-video":
            return yt_video(adapter, data)
        case "yt-channel":
            return yt_channel(adapter, data)
    return readability(adapter, data)

def yt_video(adapter, data):
    return extract_video_data(data.get('video')), 200
def yt_channel(adapter, data):
    return get_channel_info(data.get('channel')), 200
    
def readability(adapter, data):
    ip = adapter.get_client_ip()
    text = data.get("text")
    pub_key = data.get("pub")
    length = len(text)
    if length < 100 or length > 1000:
        return {'error': 'Input text must between 100 and 1000 characters long.'}, 400
    
    engine = ReadabilityEngine(text)
    encrypted = Crypto.rsa_encrypt({"fomulas": engine.calculate()}, pub_key)
    ip = Crypto.rsa_encrypt({"ip": ip}, pub_key)
    return {"f": encrypted, "i": ip}, 200
