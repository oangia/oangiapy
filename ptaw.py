from oangiapy.web import route, dispatch
from oangiapy.Youtube import extract_video_data, get_channel_info
from oangiapy.readability.ReadabilityEngine import ReadabilityEngine
from oangiapy.crypto import Crypto

@route('readability')
def readability(request):
    ip = request.get_client_ip()
    text = request.get("text")
    pub_key = request.get("pub")
    length = len(text)
    if length < 100 or length > 1000:
        return {'error': 'Input text must between 100 and 1000 characters long.'}, 400
    
    engine = ReadabilityEngine(text)
    encrypted = Crypto.rsa_encrypt({"fomulas": engine.calculate()}, pub_key)
    ip = Crypto.rsa_encrypt({"ip": ip}, pub_key)
    return {"f": encrypted, "i": ip}, 200

@route('yt-video')
def yt_video(request):
    return extract_video_data(request.get('video')), 200

@route('yt-channel')
def yt_channel(request):
    raw_info = get_channel_info(request.get('channel'))
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

        playlist_count = 0
        playlist_videos = []

        for video in playlist_entry.get('entries', []) or []:
            if not video:
                continue
        
            view_count = video.get('view_count') or 0
            duration = video.get('duration') or 0
        
            v = {
                '_type': video.get('_type', 'url'),
                'title': video.get('title'),
                'url': video.get('url') or video.get('webpage_url'),
                'view_count': view_count,
                'duration': duration,
                'thumbnails': video.get('thumbnails', []),
                'id': video.get('id')
            }
        
            playlist_videos.append(v)
        
            if v['_type'] == 'url':
                total_videos += 1
                total_views += view_count
                total_duration += duration
                playlist_count += 1
                videos_list.append(v)

        playlists.append({
            "title": playlist_entry.get('title') or "Unnamed Playlist",
            "videos": playlist_count
        })

    # Same logic as JS
    videos_list.sort(key=lambda x: x.get('view_count', 0), reverse=True)
    top_videos = videos_list[:3]

    avg_views = round(total_views / total_videos) if total_videos else 0
    avg_duration = round(total_duration / total_videos) if total_videos else 0

    # API now returns BOTH raw info AND computed analysis
    response = {
        # RAW INFO (used by <Basic info card>)
        "title": raw_info.get("title"),
        "channel": raw_info.get("channel") or raw_info.get("uploader"),
        "webpage_url": raw_info.get("webpage_url") or raw_info.get("url"),
        "uploader": raw_info.get("uploader"),
        "channel_follower_count": raw_info.get("channel_follower_count", 0),
        "playlist_count": raw_info.get("playlist_count", 0),
        "tags": raw_info.get("tags", []),

        # ANALYSIS (exact output of analyzeChannelData)
        "totalVideos": total_videos,
        "totalViews": total_views,
        "avgViews": avg_views,
        "avgDuration": avg_duration,
        "playlists": playlists,
        "topVideos": top_videos
    }

    return response, 200

# pythonanywhere
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    return dispatch(request)

if __name__ == '__main__':
    app.run()

# gcloud
import functions_framework

@functions_framework.http
def hello_http(request):
    return dispatch(request)
