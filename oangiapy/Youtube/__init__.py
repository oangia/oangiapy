import yt_dlp
import webvtt
import os
#yt-dlp https://e.streamqq.com/videos/688666971ae4c0be6a074bed/video_default.m3u8
#!pip install git+https://github.com/oangia/oangia.github.io.git#subdirectory=python&egg=oangiapy[youtube]
#from oangiapy.Youtube import download
#download("TAiGK33ckcU")
from yt_dlp import YoutubeDL
import json

def get_channel_info(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # only metadata, no video download
        'skip_download': True,
        'cookies_from_browser': '__Secure-YNID=13.YT=Hj15VR8ryg7rGNd0dUsqZIp6UOZc4ohvx5FwiV3pC1_fZoIm93_AgGSXWfEOALhzz-Vvt8xj2ALLPvlwjJh9AnWPp-vQWktqaSXw3w_jWhQQ0JXy8U7EW62yk7-2QLWzePucygcCzng0IGSfqsg2UK2SOrv7KvJU7htFXPkqw_vJrJqU-F6YCFSlKO8LC-3DPGwbt6aUyJueKP7Xhn-j6AmTAd0Y6JEx5bJyg23V_ZGhP97i2DfafsBO7dBIo-WVaCfnEqgLD3dnHEp1nGSujmc_yPncvETIG3-p44UNZMCDBbi-YmyX1yu0-X0Uf2vQLsyOME9Pk49ermRs4QJQXw; GPS=1; YSC=plV-cOsNHYw; __Secure-ROLLOUT_TOKEN=CKbXkdz9p-vy-wEQr7rrj-eWkQMY0crbkOeWkQM%3D; VISITOR_INFO1_LIVE=GJHrcOfjC-s; VISITOR_PRIVACY_METADATA=CgJWThIEGgAgWw%3D%3D; PREF=f6=40000000&tz=Asia.Ho_Chi_Minh
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    return info

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookies_from_browser': '__Secure-YNID=13.YT=Hj15VR8ryg7rGNd0dUsqZIp6UOZc4ohvx5FwiV3pC1_fZoIm93_AgGSXWfEOALhzz-Vvt8xj2ALLPvlwjJh9AnWPp-vQWktqaSXw3w_jWhQQ0JXy8U7EW62yk7-2QLWzePucygcCzng0IGSfqsg2UK2SOrv7KvJU7htFXPkqw_vJrJqU-F6YCFSlKO8LC-3DPGwbt6aUyJueKP7Xhn-j6AmTAd0Y6JEx5bJyg23V_ZGhP97i2DfafsBO7dBIo-WVaCfnEqgLD3dnHEp1nGSujmc_yPncvETIG3-p44UNZMCDBbi-YmyX1yu0-X0Uf2vQLsyOME9Pk49ermRs4QJQXw; GPS=1; YSC=plV-cOsNHYw; __Secure-ROLLOUT_TOKEN=CKbXkdz9p-vy-wEQr7rrj-eWkQMY0crbkOeWkQM%3D; VISITOR_INFO1_LIVE=GJHrcOfjC-s; VISITOR_PRIVACY_METADATA=CgJWThIEGgAgWw%3D%3D; PREF=f6=40000000&tz=Asia.Ho_Chi_Minh
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info
    
def download(id, quality = "best"):
    url = "https://www.youtube.com/watch?v=" + id
    
    ydl_opts = {
        'format': quality,
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
def download_channel(channel):
    channel_url = 'https://www.youtube.com/@' + channel +'/videos'
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    
    return info

def download_audio(id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=" + id])

def download_transcript(id):
    url = 'https://www.youtube.com/watch?v=' + id

    # Set up yt_dlp options
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,         # download manual subtitles if available
        'writeautomaticsub': True,      # fallback to auto subtitles if manual not available
        'subtitleslangs': ['en'],       # target English only
        'subtitlesformat': 'vtt',
        'outtmpl': 'transcript.%(ext)s',
        'quiet': True,
    }
    
    # Download subtitles
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return vtt_to_text("transcript.en.vtt")

def vtt_to_text(filepath):
    transcript = []
    for caption in webvtt.read(filepath):
        transcript.append(caption.text.replace("\n", " "))
    new_trans = [transcript[0]]
    for i in range(1, len(transcript)):
        if transcript[i] != new_trans[-1]:
            #print("com", transcript[i], "second", new_trans[-1])
            new_trans.append(transcript[i])
    return '\n'.join(new_trans)
