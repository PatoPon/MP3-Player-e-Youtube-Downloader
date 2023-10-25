import pygame
import threading
import yt_dlp
import os
import json
from logica import escolherMusica, escolherPasta
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from designApp import Ui_MainWindow


class MySignals(QObject):
    pronto_signal = pyqtSignal()
    musicasNaoCarregadasSignal = pyqtSignal(list)


class SuaJanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.signals = MySignals()

        self.musicasNaoCarregadas = []
        self.signals.musicasNaoCarregadasSignal.connect(
            self.musicasNaoCarregadasHandler)
        
        self.progress_bars = {}
        self.downloadLista = []
        self.baixando = False

        self.playlist = []
        self.playlist_text = "Playlist vazia"
        self.ui.progressoLabel.setText("Progresso")
        self.indice_musica_atual = 0
        self.indexOriginal = 0

        self.song_end = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.song_end)

        self.ui.botaoTocar.clicked.connect(self.playMusic)
        self.ui.botaoEscolher.clicked.connect(self.chooseMusic)
        self.ui.botaoEscolherPasta.clicked.connect(self.chooseMusicFromFolder)
        self.ui.botaoPular.clicked.connect(self.skipMusic)
        self.ui.botaoAnterior.clicked.connect(self.previousMusic)
        self.ui.botaoBaixar.clicked.connect(self.searchMusic)

        self.ui.listWidget.itemClicked.connect(self.startMusicFromClick)

        self.ui.listWidget.setDragEnabled(True)
        self.ui.listWidget.setAcceptDrops(True)
        self.ui.listWidget.setDragDropMode(QListWidget.InternalMove)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(
            lambda: self.ui.progressoLabel.setText("Progresso"))
        self.timer.setSingleShot(True)

        self.signals.pronto_signal.connect(self.iniciarTimerFimDownload)

        self.timerSlide = QtCore.QTimer(self)
        self.timerSlide.timeout.connect(self.updateSlider)
        self.timerSlide.start(1000)

        self.ui.musicaSlider.sliderReleased.connect(self.updateUserSlider)

        self.ui.listWidget.dropEvent = self.customDropEvent
        self.ui.listWidget.itemPressed.connect(self.clicked)

        self.timerCaixaDeTexto = QtCore.QTimer(self)
        self.timerCaixaDeTexto.timeout.connect(
            lambda: self.musicasNaoCarregadasHandler(self.musicasNaoCarregadas))
        self.timerCaixaDeTexto.setSingleShot(True)

        self.load_playlist()
    
    def iniciarTimerFimDownload(self):
            self.timer.start(5000)

    def musicasNaoCarregadasHandler(self, musicasNaoCarregadas):
        message = "As seguintes músicas não puderam ser carregadas:\n\n"
        message += "\n".join(musicasNaoCarregadas)

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Músicas não carregadas")
        msg_box.setText(message)
        msg_box.exec_()

    def save_playlist(self):
        print(self.indice_musica_atual)
        data = {
            "playlist": self.playlist,
            "indice_musica_atual": self.indice_musica_atual
        }

        with open('playlist.json', 'w') as file:
            json.dump(data, file, indent=1)

    def load_playlist(self):
        try:
            with open('playlist.json', 'r') as file:
                data = json.load(file)

            playlist = data.get('playlist', [])
            updated_playlist = []

            for item in playlist:
                try:
                    if os.path.exists(item['path']):
                        updated_playlist.append(item)
                    else:
                        self.musicasNaoCarregadas.append(item['nome_musica'])
                except Exception as e:
                    self.musicasNaoCarregadas.append(item['nome_musica'])
                    print(
                        f"Erro ao verificar a música '{item['nome_musica']}'")

            self.indice_musica_atual = data.get('indice_musica_atual', 0)

            if self.musicasNaoCarregadas:
                self.timerCaixaDeTexto.start(500)

            self.playlist = updated_playlist
            self.updatePlaylistLabel()

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def clicked(self, item):
        self.indexOriginal = self.ui.listWidget.row(item)

    def customDropEvent(self, event):
        drop_position = event.pos()
        dropped_item = self.ui.listWidget.itemAt(drop_position)

        if dropped_item:
            original_index = self.playlist.index(
                self.playlist[self.indexOriginal])
            dropped_index = self.ui.listWidget.row(dropped_item)

            if dropped_index is not None and 0 <= dropped_index < len(self.playlist) and original_index != dropped_index:
                self.playlist[original_index], self.playlist[dropped_index] = self.playlist[dropped_index], self.playlist[original_index]
                self.updatePlaylistLabel()

    def updateUserSlider(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            position = self.ui.musicaSlider.value()
            pygame.mixer.music.set_pos(position)
            pygame.mixer.music.unpause()

    def updateSlider(self):
        self.ui.listWidget.clearFocus()
        if pygame.mixer.music.get_busy():
            self.ui.botaoTocar.setIcon(QtGui.QIcon('parar.png'))
            self.ui.musicaTocando.setText(
                self.playlist[self.indice_musica_atual]['nome_musica'])
            self.ui.musicaSlider.setValue(self.ui.musicaSlider.value() + 1)
        else:
            self.ui.botaoTocar.setIcon(QtGui.QIcon('reproduzir.png'))
            try:
                self.ui.musicaTocando.setText(
                    self.playlist[self.indice_musica_atual]['nome_musica'])
            except:
                pass
        
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setSelected(i == self.indice_musica_atual)

        for event in pygame.event.get():
            if event.type == self.song_end:
                self.skipMusic()

    def playMusic(self):
        if not pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() > 0:
                self.ui.botaoTocar.setIcon(QtGui.QIcon('parar.png'))
                pygame.mixer.music.unpause()
            elif self.playlist:
                self.ui.botaoTocar.setIcon(QtGui.QIcon('reproduzir.png'))
                pygame.mixer.music.load(
                    self.playlist[self.indice_musica_atual]['path'])
                self.ui.musicaSlider.setValue(0)
                self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                    self.playlist[self.indice_musica_atual]['path']).get_length()))
                self.ui.musicaTocando.setText(
                    self.playlist[self.indice_musica_atual]['nome_musica'])
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
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(
                self.playlist[self.indice_musica_atual]['nome_musica'])
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
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(
                self.playlist[self.indice_musica_atual]['nome_musica'])
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
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(
                self.playlist[self.indice_musica_atual]['nome_musica'])
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

    def downloadMusic(self):
        while self.downloadLista:
            musica = self.downloadLista[0]
            self.ui.progressoLabel.setText(f"Pesquisando {musica}")

            self.baixando = True

            def progress_callback(status, termo):
                match status['status']:
                    case 'downloading':
                        self.ui.progressoLabel.setText(f"Baixando {termo}")
                        if 'downloaded_bytes' in status and 'total_bytes' in status:
                            downloaded = status['downloaded_bytes']
                            total = status['total_bytes']
                            if total > 0:
                                percentual = int((downloaded / total) * 100)
                                self.ui.BarraDeProgresso.setValue(percentual)  
                    case 'finished':
                        self.ui.progressoLabel.setText(f"Convertendo {termo}")
                    case _:
                        self.ui.progressoLabel.setText(f"Processando {termo}")

            ydl_opts = {
                'format': 'bestaudio/best',
                'default_search': "ytsearch",
                'progress_hooks': [(lambda termo: lambda s: progress_callback(s, termo))(musica)],
                'match-filter': 'is-video',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(musica, download=False)
                ydl.download([musica])

                webm_name = ydl.prepare_filename(info_dict)
                nome_base, extensao = os.path.splitext(webm_name)

                if not os.path.exists(webm_name):
                    self.ui.progressoLabel.setText(f"{nome_base}.mp3 foi baixado!")
                    self.ui.downloadList.takeItem(0)
                    self.downloadLista.remove(musica)
        
        if self.downloadLista:
            downloadThread = threading.Thread(target=self.downloadMusic)
            downloadThread.start()
            self.baixando = True

        self.ui.progressoLabel.setText("Todas as músicas foram baixadas!")
        self.baixando = False
        self.signals.pronto_signal.emit()


    def searchMusic(self):
        termo_pesquisa, _ = QInputDialog.getText(
            None, "Digite o termo de pesquisa", "Digite o nome da música ou artista:")
        if termo_pesquisa:
            self.downloadLista.append(termo_pesquisa)
            self.ui.downloadList.addItem(termo_pesquisa)
        
            if self.downloadLista and self.baixando == False:
                downloadThread = threading.Thread(target=self.downloadMusic)
                downloadThread.start()
                self.baixando = True

    def chooseMusic(self):
        self.playlist = escolherMusica(self.playlist)
        self.updatePlaylistLabel()
        self.save_playlist()
    
    def chooseMusicFromFolder(self):
        self.playlist = escolherPasta(self.playlist)
        self.updatePlaylistLabel()
        self.save_playlist()


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    app = QtWidgets.QApplication([])
    window = SuaJanelaPrincipal()
    window.show()
    app.aboutToQuit.connect(window.save_playlist)
    app.exec()
    pygame.quit()
