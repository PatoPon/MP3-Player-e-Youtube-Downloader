import os
import yt_dlp
from youtube_search import YoutubeSearch
import sys
import vlc

ydl_opts = {
    'format': 'bestaudio/best',
    'default-search': "ytsearch",
    'outtmpl': '%(uploader)s - %(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

tituloVideo = ""

def procurarMusica(musica):

    if 'youtube.com' in musica:
        url = musica
    else:
        search_results = YoutubeSearch(musica, max_results=1)
        try:
            url = f"https://www.youtube.com{search_results.videos[0]['url_suffix']}"
        except Exception as error:
            print("Video não existe ou o URL está errado!")
            sys.exit(1)
    
    return url

def downloadMusica(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video = ydl.extract_info(url, download=False)

        tituloVideo = f"{video.get('uploader', None)} - {video.get('title', None)}"

        if not os.path.isfile(f"{tituloVideo}.mp3"):
            ydl.download([url])
            print(f"Música '{tituloVideo}' baixado com sucesso em formato MP3.")
        else:
            print(f"O arquivo '{tituloVideo}.mp3' já existe. Não foi necessário fazer o download.")
        
        return tituloVideo