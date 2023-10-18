import pygame, threading, yt_dlp, os
from logica import escolherMusica
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from designApp import Ui_MainWindow

class MySignals(QObject):
    pronto_signal = pyqtSignal()

class SuaJanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.signals = MySignals()

        self.playlist = []
        self.playlist_text = "Playlist vazia"
        self.ui.progressoLabel.setText("Progresso")
        self.indice_musica_atual = 0
        self.indexOriginal = 0

        self.song_end = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.song_end)

        self.ui.botaoTocar.clicked.connect(self.playMusic)
        self.ui.botaoEscolher.clicked.connect(self.chooseMusic)
        self.ui.botaoPular.clicked.connect(self.skipMusic)
        self.ui.botaoAnterior.clicked.connect(self.previousMusic)
        self.ui.botaoBaixar.clicked.connect(self.searchMusic)

        self.ui.listWidget.itemClicked.connect(self.startMusicFromClick)

        self.ui.listWidget.setDragEnabled(True)
        self.ui.listWidget.setAcceptDrops(True)
        self.ui.listWidget.setDragDropMode(QListWidget.InternalMove)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.ui.progressoLabel.setText("Progresso"))
        self.timer.setSingleShot(True)

        self.signals.pronto_signal.connect(lambda: self.timer.start(5000))

        self.timerSlide = QtCore.QTimer(self)
        self.timerSlide.timeout.connect(self.updateSlider)
        self.timerSlide.start(1000)

        self.ui.musicaSlider.sliderReleased.connect(self.updateUserSlider)

        self.ui.listWidget.dropEvent = self.customDropEvent
        self.ui.listWidget.itemPressed.connect(self.clicked)

    def clicked(self, item):
        self.indexOriginal = self.ui.listWidget.row(item)

    def customDropEvent(self, event):
        drop_position = event.pos()
        dropped_item = self.ui.listWidget.itemAt(drop_position)

        if dropped_item:
            original_index = self.playlist.index(self.playlist[self.indexOriginal])
            dropped_index = self.ui.listWidget.row(dropped_item)

            if dropped_index is not None and 0 <= dropped_index < len(self.playlist) and original_index != dropped_index:
                self.playlist[original_index], self.playlist[dropped_index] = self.playlist[dropped_index], self.playlist[original_index]
                self.updatePlaylistLabel()

    def updateUserSlider(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(self.playlist[self.indice_musica_atual]['path']).get_length()))
            position = self.ui.musicaSlider.value()
            pygame.mixer.music.set_pos(position)
            pygame.mixer.music.unpause()

    def updateSlider(self):
        if pygame.mixer.music.get_busy():
            self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            self.ui.musicaSlider.setValue(self.ui.musicaSlider.value() + 1)
        else:
            try:
                self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            except:
                self.ui.musicaTocando.setText("Nenhuma música selecionada")

        for event in pygame.event.get():
            if event.type == self.song_end:
                self.skipMusic()

    def playMusic(self):
        if not pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.unpause()
            elif self.playlist:
                pygame.mixer.music.load(self.playlist[self.indice_musica_atual]['path'])
                self.ui.musicaSlider.setValue(0)
                self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(self.playlist[self.indice_musica_atual]['path']).get_length()))
                self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
                pygame.mixer.music.play()

                for i in range(self.ui.listWidget.count()):
                    item = self.ui.listWidget.item(i)
                    item.setSelected(i == self.indice_musica_atual)
        else:
            pygame.mixer.music.pause()

    def skipMusic(self):
        if self.playlist:
            if hasattr(self, 'indice_musica_atual'):
                if self.indice_musica_atual + 1 < len(self.playlist):
                    self.indice_musica_atual += 1
                else:
                    self.indice_musica_atual = 0
            else:
                self.indice_musica_atual = 0

            next_music_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(next_music_path)
            self.ui.musicaSlider.setValue(0)
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            pygame.mixer.music.play()

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setSelected(i == self.indice_musica_atual)

    def previousMusic(self):
        if self.playlist:
            pygame.mixer.music.pause()

            if hasattr(self, 'indice_musica_atual') and self.indice_musica_atual > 0:
                self.indice_musica_atual -= 1
            else:
                self.indice_musica_atual = len(self.playlist) - 1

            previous_music_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(previous_music_path)
            self.ui.musicaSlider.setValue(0)
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            pygame.mixer.music.play()

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setSelected(i == self.indice_musica_atual)

    def startMusicFromClick(self, item):
        self.ui.listWidget.clearFocus()
        index = self.ui.listWidget.row(item)
        if index < len(self.playlist):
            pygame.mixer.music.pause()
            self.indice_musica_atual = index
            next_music_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(next_music_path)
            self.ui.musicaSlider.setValue(0)
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            pygame.mixer.music.play()

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setSelected(i == self.indice_musica_atual)

    def updatePlaylistLabel(self):
        self.ui.listWidget.clear()
        for index, item in enumerate(self.playlist):
            music_name = item['nome_musica']
            self.ui.listWidget.addItem(f"{index + 1}. {music_name}")
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setSelected(i == self.indice_musica_atual)

    def downloadMusic(self, url):
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

            webm_name = ydl.prepare_filename(ydl.extract_info(url))

            if not os.path.exists(webm_name):
                self.ui.progressoLabel.setText("Pronto!")
                self.signals.pronto_signal.emit()

    def searchMusic(self):
        termo_pesquisa, _ = QInputDialog.getText(None, "Digite o termo de pesquisa", "Digite o nome da música ou artista:")
        if termo_pesquisa:
            threading.Thread(target=self.downloadMusic, args=(termo_pesquisa,)).start()

    def chooseMusic(self):
        self.playlist = escolherMusica(self.playlist)
        self.updatePlaylistLabel()
        self.playMusic()

if __name__ == '__main':
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    app = QtWidgets.QApplication([])
    window = SuaJanelaPrincipal()
    window.show()
    app.exec()
    pygame.quit()