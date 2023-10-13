import tkinter as tk
from tkinter import filedialog, simpledialog, Label
import os
import vlc
import yt_dlp
from youtube_search import YoutubeSearch
import sys
import threading

musica = "hello.mp3"
instancia = vlc.Instance("--no-video")
player = instancia.media_player_new()

def tocarMusica(player, musica):
    if os.path.exists(musica):
        media = instancia.media_new(musica)
        player.set_media(media)
        player.play()
    else:
        mensagem_erro = "O arquivo de música não foi encontrado."
        tk.messagebox.showerror("Erro", mensagem_erro)

def pararMusica(player):
    player.stop()

def escolherMusica():
    global musica
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos MP3", "*.mp3")])
    if file_path:
        musica = file_path

def baixarMusica():
    global musica
    termo_pesquisa = simpledialog.askstring("Digite o termo de pesquisa", "Digite o nome da música ou artista:")
    if termo_pesquisa:
        percent_label.config(text="Iniciando pesquisa...")  # Defina um texto inicial
        threading.Thread(target=procurarMusica, args=(termo_pesquisa,)).start()

def procurarMusica(termo_pesquisa):
    search_results = YoutubeSearch(termo_pesquisa, max_results=1)
    url = f"https://www.youtube.com{search_results.videos[0]['url_suffix']}"
    downloadMusica(url)

def downloadMusica(url):
    def progress_callback(status):
        if status['status'] == 'downloading':
            percent = status['_percent_str']
            percent_label.config(text=f"Baixando: {percent}")
        elif status['status'] == 'finished':
            percent_label.config(text="Iniciando conversão...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'default-search': "ytsearch",
        'progress_hooks': [progress_callback],
        'outtmpl': '%(uploader)s - %(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

        nome_webm = ydl.prepare_filename(ydl.extract_info(url))
        nome_mp3 = nome_webm.replace(".webm", ".mp3")

        if not os.path.exists(nome_webm):
            global musica
            percent_label.config(text="O arquivo está pronto!")
            musica = nome_mp3

janela = tk.Tk()
janela.title("Programa de Música")
janela.geometry("400x200")

percent_label = Label(janela, text="", font=("Helvetica", 14))
percent_label.pack()

play_music_button = tk.Button(janela, text="Tocar Música", state="active")
play_music_button.config(command=lambda: tocarMusica(player, musica))
play_music_button.pack()

stop_music_button = tk.Button(janela, text="Parar Música", state="active")
stop_music_button.config(command=lambda: pararMusica(player))
stop_music_button.pack()

botaoEscolherMusica = tk.Button(janela, text="Escolher Música", state="active")
botaoEscolherMusica.config(command=escolherMusica)
botaoEscolherMusica.pack()

botaoBaixarMusica = tk.Button(janela, text="Baixar Música", state="active")
botaoBaixarMusica.config(command=baixarMusica)
botaoBaixarMusica.pack()

janela.mainloop()