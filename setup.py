from setuptools import setup, find_packages

setup(
    name='oangiapy',
    version='0.1',
    install_requires=[
        
    ],
    extras_require={
        'api': ['cryptography==46.0.3'],
        'web': ['requests', "pymongo", "firebase-admin"],
        'youtube': ['yt-dlp', 'webvtt-py'],
        'video': ['pydub', 'moviepy==1.0.3'],
        'tts': ['gTTS', 'SpeechRecognition'],
        'all': ['pytest', 'black', 'torch'],
        'gg_sheet': ['gspread', 'pandas']
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "oangiapy.web": ["templates/*", "static/*"]
    }
)
