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
    """Return pre-processed channel stats in the same structure as analyzeChannelData()."""

    raw_info = get_channel_info(data.get('channel'))
    if not raw_info:
        return {'error': 'Could not extract channel information'}, 404

    total_videos = 0
    total_views = 0
    total_duration = 0
    playlists = []
    videos_list = []

    entries = raw_info.get('entries', [])

    for playlist_entry in entries:
        if not playlist_entry:
            continue

        playlist_videos = []
        playlist_count = 0

        for video in playlist_entry.get('entries', []) or []:
            if not video:
                continue

            v = {
                '_type': video.get('_type', 'url'),
                'title': video.get('title'),
                'url': video.get('url') or video.get('webpage_url'),
                'view_count': video.get('view_count', 0),
                'duration': video.get('duration', 0),
                'thumbnails': video.get('thumbnails', []),
                'id': video.get('id')
            }

            if v['_type'] == 'url':
                total_videos += 1
                total_views += v['view_count']
                total_duration += v['duration']
                videos_list.append(v)
                playlist_count += 1

            playlist_videos.append(v)

        playlists.append({
            "title": playlist_entry.get('title') or "Unnamed Playlist",
            "videos": playlist_count
        })

    # Same sorting & slicing as JS
    videos_list.sort(key=lambda x: x.get('view_count', 0), reverse=True)
    top_videos = videos_list[:3]

    avg_views = round(total_views / total_videos) if total_videos else 0
    avg_duration = round(total_duration / total_videos) if total_videos else 0

    # EXACT structure as analyzeChannelData() return
    response = {
        "totalVideos": total_videos,
        "totalViews": total_views,
        "avgViews": avg_views,
        "avgDuration": avg_duration,
        "playlists": playlists,
        "topVideos": top_videos,
    }

    return response, 200
    
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
