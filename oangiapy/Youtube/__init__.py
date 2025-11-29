import yt_dlp
import webvtt
import os
#yt-dlp https://e.streamqq.com/videos/688666971ae4c0be6a074bed/video_default.m3u8
#!pip install git+https://github.com/oangia/oangia.github.io.git#subdirectory=python&egg=oangiapy[youtube]
#from oangiapy.Youtube import download
#download("TAiGK33ckcU")
from yt_dlp import YoutubeDL
import json
import tempfile

# Your cookie string in Netscape format
cookies_string = "__Secure-YNID=13.YT=pjuycVULBqnLpPtYkHMuDx8W1OiggOClJLys5Z5gYSxQTXxaPQpc7VTZlhg-MIm2MEVsBTeYqFDr9S6fFnrZ0o3FGzuGG9WH2Efmfc1PEvV_VPT1EJNBb9c9LwmJGWexgFO_ioZuoijH-ap_WEMT04fQM8HV5-ZDfWaviJXLoJsKBtVsT8-CJVbcaZA_oI0nUWxYhOKREV50hjpN8K1yawafjK3PurfI75x5-scOks6Ahorj9hevojsQPj_9Xz_XyF_sEH55gdoyO0O4GaZ6UNs0RNvR8TIGwrxVzmVNA-zPIWmzPzGeUzqr2PRNlgwmzhOmJRlLsKDai8EzykP__g; GPS=1; YSC=81hGz0Fo7aE; VISITOR_INFO1_LIVE=cP3MHJ-L4Kw; VISITOR_PRIVACY_METADATA=CgJWThIEGgAgIA%3D%3D; __Secure-ROLLOUT_TOKEN=CP-80ZPYpee5XRDBzZSy6paRAxjM-oKz6paRAw%3D%3D; PREF=f6=40000000&tz=Asia.Ho_Chi_Minh"

def get_channel_info(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # only metadata, no video download
        'skip_download': True,
        'cookies_from_browser': 'chrome'
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    return info

def get_video_info(url):
    # Write to a temporary file
    # Convert to Netscape format
    lines = ["# Netscape HTTP Cookie File"]  # <--- header required
    for pair in cookie_str.split('; '):
        if '=' in pair:
            name, value = pair.split('=', 1)
            # Format: domain, TRUE/FALSE, path, secure, expiration, name, value
            lines.append(f".youtube.com\tTRUE\t/\tFALSE\t0\t{name}\t{value}")
    
    netscape_cookies = "\n".join(lines)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write(netscape_cookies)
        cookie_file = f.name
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
