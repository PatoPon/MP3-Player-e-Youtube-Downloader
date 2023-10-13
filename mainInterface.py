import tkinter as tk
from tkinter import filedialog
import mainLogica
import vlc
import os

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
    musica = tk.simpledialog.askstring("Digite a música", "Nome ou URL da música:")
    url = mainLogica.procurarMusica(musica)
    musica = mainLogica.downloadMusica(url)

janela = tk.Tk()
janela.title("Programa de Música")
janela.geometry("800x600")

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

# Iniciar a interface
janela.mainloop()