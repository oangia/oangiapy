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
    """Extract and return structured YouTube channel data matching the JS structure."""
    
    # Get raw channel info
    raw_info = get_channel_info(data.get('channel'))
    
    if not raw_info:
        return {'error': 'Could not extract channel information'}, 404
    
    # Extract playlist entries (each playlist contains videos)
    entries = raw_info.get('entries', [])
    structured_entries = []
    
    for playlist_entry in entries:
        if playlist_entry:
            # Each entry is a playlist with nested videos
            playlist_videos = []
            
            # Check if this playlist has video entries
            if playlist_entry.get('entries'):
                for video in playlist_entry.get('entries', []):
                    if video:
                        playlist_videos.append({
                            '_type': video.get('_type', 'url'),
                            'title': video.get('title'),
                            'url': video.get('url') or video.get('webpage_url'),
                            'view_count': video.get('view_count', 0),
                            'duration': video.get('duration', 0),
                            'thumbnails': video.get('thumbnails', []),
                            'id': video.get('id')
                        })
            
            # Add the playlist with its videos
            structured_entries.append({
                'title': playlist_entry.get('title'),
                'entries': playlist_videos
            })
    
    # Return structured data matching the JS expectations
    structured_response = {
        'title': raw_info.get('title'),
        'channel': raw_info.get('channel') or raw_info.get('uploader'),
        'webpage_url': raw_info.get('webpage_url') or raw_info.get('url'),
        'uploader': raw_info.get('uploader'),
        'channel_follower_count': raw_info.get('channel_follower_count', 0),
        'playlist_count': raw_info.get('playlist_count', 0),
        'tags': raw_info.get('tags', []),
        'entries': structured_entries
    }
    
    return structured_response, 200
    
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
