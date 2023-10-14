import sys
import os
import vlc
import yt_dlp
import threading
from youtube_search import YoutubeSearch
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QLabel, QPushButton, QFileDialog, QSlider, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

# Definir a aparência dos botões e rótulos
def set_button_style(button):
    button.setStyleSheet(
        "QPushButton {"
        "background-color: #2196F3;"
        "border: none;"
        "color: white;"
        "padding: 10px 15px;"
        "border-radius: 5px;"
        "font-size: 16px;"
        "}"
        "QPushButton:hover {"
        "background-color: #1976D2;"
        "}"
    )

def set_label_style(label):
    label.setAlignment(Qt.AlignCenter)
    label.setFont(QFont("Arial", 14, QFont.Bold))

# Inicializar a instância VLC e o reprodutor de mídia
instancia = vlc.Instance("--no-video")
player = instancia.media_player_new()

# Inicializar a música como "hello.mp3"
musica = "hello.mp3"

# Função para tocar a música
def tocarMusica(player, musica):
    if os.path.exists(musica):
        media = instancia.media_new(musica)
        player.set_media(media)
        player.play()
        # Iniciar o temporizador para atualizar o slider
        slider_timer.start(1000)  # Atualizar a cada segundo
    else:
        mensagem_erro = "O arquivo de música não foi encontrado."
        print("Erro:", mensagem_erro)

# Função para parar a música
def pararMusica(player):
    player.stop()
    # Parar o temporizador quando a música é parada
    slider_timer.stop()

# Função para escolher uma música
def escolherMusica():
    global musica
    file_path, _ = QFileDialog.getOpenFileName(None, "Escolher Música", "", "Arquivos MP3 (*.mp3)")
    if file_path:
        musica = file_path

# Função para baixar uma música do YouTube
def baixarMusica():
    global musica
    termo_pesquisa, _ = QInputDialog.getText(None, "Digite o termo de pesquisa", "Digite o nome da música ou artista:")
    if termo_pesquisa:
        percent_label.setText("Iniciando pesquisa...")
        threading.Thread(target=procurarMusica, args=(termo_pesquisa,)).start()

# Função para procurar música no YouTube
def procurarMusica(termo_pesquisa):
    search_results = YoutubeSearch(termo_pesquisa, max_results=1)
    url = f"https://www.youtube.com{search_results.videos[0]['url_suffix']}"
    downloadMusica(url)

# Função para fazer o download da música do YouTube
def downloadMusica(url):
    def progress_callback(status):
        if status['status'] == 'downloading':
            percent = status['_percent_str']
            percent_label.setText(f"Baixando: {percent}")
        elif status['status'] == 'finished':
            percent_label.setText("Iniciando conversão...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': "ytsearch",
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
            percent_label.setText("O arquivo está pronto!")
            musica = nome_mp3

# Função para atualizar o slider com base na posição da música
def update_slider():
    if player.is_playing():
        # Obter a posição atual da música em milissegundos
        position = player.get_time()
        duration = player.get_length()
        if duration > 0:
            # Calcular a posição como uma porcentagem da duração
            position_percentage = (position / duration) * 100

            # Calcular o tempo decorrido e o tempo total
            elapsed_time = position / 1000  # em segundos
            total_time = duration / 1000  # em segundos

            # Formatando os tempos decorridos e totais como minutos:segundos
            elapsed_time_str = "{:02d}:{:02d}".format(int(elapsed_time // 60), int(elapsed_time % 60))
            total_time_str = "{:02d}:{:02d}".format(int(total_time // 60), int(total_time % 60))

            # Atualizar o rótulo com a duração decorrida e total
            percent_label.setText(f"Duração: {elapsed_time_str} / {total_time_str}")

            # Atualizar o slider
            music_slider.setValue(int(position_percentage))

def set_music_position(position):
    if player.get_media() is not None:
        duration = player.get_media().get_duration()
        if duration > 0:
            # Calcule a posição em milissegundos com base na porcentagem do slider
            position_ms = (position / 100) * duration
            player.set_time(int(position_ms))

            # Se a música não estiver tocando ou estiver pausada, inicie a reprodução a partir da nova posição
            if not player.is_playing() or player.get_state() == vlc.State.Ended:
                player.play()

# Inicialização da aplicação Qt
app = QApplication(sys.argv)

# Configuração da janela
janela = QWidget()
janela.setWindowTitle("Programa de Música / Youtube Downloader")
janela.setGeometry(100, 100, 400, 300)
janela.setWindowIcon(QIcon("icon.png"))

layout = QVBoxLayout()

# Rótulo para exibir o progresso
percent_label = QLabel()
set_label_style(percent_label)
layout.addWidget(percent_label)

# Botões para controlar a música
play_music_button = QPushButton("Tocar Música")
set_button_style(play_music_button)
play_music_button.clicked.connect(lambda: tocarMusica(player, musica))
layout.addWidget(play_music_button)

stop_music_button = QPushButton("Parar Música")
set_button_style(stop_music_button)
stop_music_button.clicked.connect(lambda: pararMusica(player))
layout.addWidget(stop_music_button)

# Botões para escolher e baixar música
botaoEscolherMusica = QPushButton("Escolher Música")
set_button_style(botaoEscolherMusica)
botaoEscolherMusica.clicked.connect(escolherMusica)
layout.addWidget(botaoEscolherMusica)

botaoBaixarMusica = QPushButton("Baixar Música")
set_button_style(botaoBaixarMusica)
botaoBaixarMusica.clicked.connect(baixarMusica)
layout.addWidget(botaoBaixarMusica)

# Slider para controlar a posição da música
music_slider = QSlider(Qt.Horizontal)
layout.addWidget(music_slider)

# Criando um temporizador para atualizar o slider automaticamente
slider_timer = QTimer()
slider_timer.timeout.connect(update_slider)

# Conectar o evento sliderMoved ao método set_music_position
music_slider.sliderMoved.connect(set_music_position)

# Configuração da janela principal
janela.setLayout(layout)
janela.show()

sys.exit(app.exec_())