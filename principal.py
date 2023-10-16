from designApp import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow
from logica import *
import math
import pygame  # Importe o Pygame
import yt_dlp
import threading


class MySignals(QObject):
    pronto_signal = pyqtSignal()


class SuaJanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crie uma instância da classe Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.signals = MySignals()

        self.playlist = []  # Inicialize a lista de reprodução
        self.playlist_text = "Playlist vazia"
        self.ui.progressoLabel.setText("Progresso")
        self.indice_musica_atual = 0

        self.SONG_END = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.SONG_END)

        # Agora você pode interagir com os elementos da interface
        self.ui.botaoTocar.clicked.connect(self.tocarMusica)
        self.ui.botaoParar.clicked.connect(self.pararMusica)
        self.ui.botaoEscolher.clicked.connect(self.escolherMusica)
        self.ui.botaoPular.clicked.connect(self.pularMusica)
        self.ui.botaoAnterior.clicked.connect(self.anteriorMusicaMusica)
        self.ui.botaoBaixar.clicked.connect(self.procurarMusica)

        self.ui.listWidget.itemClicked.connect(self.iniciarMusicaClicada)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.ui.progressoLabel.setText(
            "Progresso"))  # Conecte o slot de redefinição
        self.timer.setSingleShot(True)

        self.timerSlide = QtCore.QTimer(self)
        self.timerSlide.start(1)
        self.timerSlide.timeout.connect(self.atualizarSlider)

        self.signals.pronto_signal.connect(lambda:
                                           self.timer.start(5000)
                                           )

    def tocarMusica(self):
        if not pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.unpause()
            elif self.playlist:
                pygame.mixer.music.load(
                    self.playlist[self.indice_musica_atual]['path'])
                duracao_musica = math.floor(pygame.mixer.Sound(
                    self.playlist[self.indice_musica_atual]['path']).get_length())
                self.ui.musicaSlider.setMaximum(duracao_musica)
                pygame.mixer.music.play()
        else:
            pass

    def atualizarSlider(self):
        if pygame.mixer.music.get_busy():
            tempo_atual = pygame.mixer.music.get_pos() // 1000
            self.ui.musicaSlider.setValue(tempo_atual)
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.pularMusica()

    def pularMusica(self):
        if self.playlist:
            # Pare a música atual, se estiver tocando
            pygame.mixer.music.pause()

            # Verifique se chegamos ao final da playlist
            if hasattr(self, 'indice_musica_atual'):
                if self.indice_musica_atual + 1 < len(self.playlist):
                    self.indice_musica_atual += 1
                else:
                    # Volte para a primeira música
                    self.indice_musica_atual = 0
            else:
                # Se é a primeira vez, comece com a primeira música
                self.indice_musica_atual = 0

            proxima_musica_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(proxima_musica_path)
            duracao_musica = math.floor(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length())
            self.ui.musicaSlider.setMaximum(duracao_musica)
            pygame.mixer.music.play()

    def anteriorMusica(self):
        if self.playlist:
            pygame.mixer.music.pause()

            if hasattr(self, 'indice_musica_atual') and self.indice_musica_atual > 0:
                self.indice_musica_atual -= 1
            else:
                self.indice_musica_atual = len(self.playlist) - 1

            musica_anterior_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(musica_anterior_path)
            duracao_musica = math.floor(pygame.mixer.Sound(musica_anterior_path).get_length())
            self.ui.musicaSlider.setMaximum(duracao_musica)
            pygame.mixer.music.play()

    def iniciarMusicaClicada(self, item):
        index = self.ui.listWidget.row(item)
        if index < len(self.playlist):
            pygame.mixer.music.pause()
            self.indice_musica_atual = index
            print(self.indice_musica_atual)
            proxima_musica_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(proxima_musica_path)
            duracao_musica = math.floor(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length())
            self.ui.musicaSlider.setMaximum(duracao_musica)
            pygame.mixer.music.play()

    def pararMusica(self):
        pygame.mixer.music.pause()

    def atualizarPlaylistLabel(self):
        self.ui.listWidget.clear()

        for index, item in enumerate(self.playlist):
            nome_musica = item['nome_musica']
            self.ui.listWidget.addItem(f"{index + 1}. {nome_musica}")

    def baixarMusica(self, url):
        self.ui.progressoLabel.setText("Pesquisando")

        def progress_callback(status):
            if status['status'] == 'downloading':
                self.ui.progressoLabel.setText(f"Baixando")
                if 'downloaded_bytes' in status and 'total_bytes' in status:
                    downloaded = status['downloaded_bytes']
                    total = status['total_bytes']
                    if total > 0:
                        progress_percent = int((downloaded / total) * 100)
                        self.ui.BarraDeProgresso.setValue(progress_percent)
            elif status['status'] == 'finished':
                self.ui.progressoLabel.setText("Convertendo")
            else:
                self.ui.progressoLabel.setText("Processando")

        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': "ytsearch",
            'progress_hooks': [progress_callback],
            'match-filter': 'is-video',
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

            if not os.path.exists(nome_webm):
                self.ui.progressoLabel.setText("Pronto!")
                self.signals.pronto_signal.emit()

    def procurarMusica(self):
        termo_pesquisa, _ = QInputDialog.getText(
            None, "Digite o termo de pesquisa", "Digite o nome da música ou artista:")
        if termo_pesquisa:
            threading.Thread(target=self.baixarMusica,
                             args=(termo_pesquisa,)).start()

    def escolherMusica(self):
        self.playlist = escolherMusica(self.playlist)
        self.atualizarPlaylistLabel()
        self.tocarMusica()

if __name__ == '__main__':
    pygame.init()  # Inicialize o Pygame
    app = QtWidgets.QApplication([])
    window = SuaJanelaPrincipal()
    window.show()
    app.exec()
    pygame.quit()  # Finalize o Pygame quando a aplicação encerrar
