import pygame
import yt_dlp
import os
import json
import random
from logica import escolherMusica, escolherPasta, escolherPastaDownload
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from designApp import Ui_MainWindow


class sinaisMusicas(QObject):
    pronto_signal = pyqtSignal()
    musicasNaoCarregadasSignal = pyqtSignal(list)


class DownloadThread(QThread):
    progressoSignal = pyqtSignal(str)
    updateDownloadSignal = pyqtSignal(int)
    updateDownloadFolderSignal = pyqtSignal(str)

    def __init__(self, downloadLista, parent=None):
        super().__init__(parent)
        self.downloadFolder = "./Músicas"
        self.downloadLista = downloadLista

    def run(self):
        while self.downloadLista:
            musica = self.downloadLista[0]
            self.progressoSignal.emit(f"Pesquisando {musica}")

            def progress_callback(status):
                match status['status']:
                    case 'downloading':
                        self.progressoSignal.emit(f"Baixando {musica}")
                        if 'downloaded_bytes' in status and 'total_bytes' in status:
                            downloaded = status['downloaded_bytes']
                            total = status['total_bytes']

                            if total > 0:
                                percentual = int((downloaded / total) * 100)
                                self.progressoSignal.emit(
                                    f"Baixando {musica} ({percentual}%)")

                    case 'finished':
                        self.progressoSignal.emit(f"Convertendo {musica}")
                    case _:
                        self.progressoSignal.emit(f"Processando {musica}")

            ydl_opts = {
                'format': 'bestaudio/best',
                'default_search': 'ytsearch',
                'progress_hooks': [(lambda status: progress_callback(status))],
                'outtmpl': self.downloadFolder+'/%(title)s.%(ext)s',
                'postprocessors': [
                    {
                        'key': 'FFmpegMetadata',
                        'add_metadata': True
                    },
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(musica, download=False)
                if info_dict.get('entries'):
                    if 'extractor' in info_dict and info_dict['extractor'] == 'youtube:playlist':
                        self.progressoSignal.emit(
                            f"Playlists não são suportadas: {musica}")
                    else:
                        musica = info_dict['entries'][0]['title']
                        self.downloadLista[0] = musica
                        self.updateDownloadSignal.emit(self)

                webmNome = ydl.prepare_filename(info_dict)

                ydl.download([musica])

                if not os.path.exists(webmNome):
                    self.progressoSignal.emit(f"{musica}.mp3 foi baixado!")
                    self.downloadLista.remove(musica)
                    self.updateDownloadSignal.emit(self)

        self.progressoSignal.emit("Todas as músicas foram baixadas!")


class CaixaDeDialogo(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)

        # Defina o estilo da caixa de diálogo
        estilo_caixa_de_dialogo = """
        QDialog {
            background-color: #800080;
        }
        QLabel {
            color: white;
        }
        QLineEdit {
            background-color: #444;
            color: white;
        }
        QPushButton {
            background-color: #007acc;
            color: white;
        }
        QPushButton:hover {
            background-color: #005faa;
        }
        """

        self.setStyleSheet(estilo_caixa_de_dialogo)

        # Crie os elementos da interface do usuário
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()

        self.label = QLabel(message)
        self.input = QLineEdit()
        self.button = QPushButton("OK")

        self.button.clicked.connect(self.accept)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)


class SuaJanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.signals = sinaisMusicas()

        self.musicasNaoCarregadas = []
        self.signals.musicasNaoCarregadasSignal.connect(
            self.musicasNaoCarregadasHandler)

        self.downloadLista = []

        self.playlist = []
        self.ui.progressoLabel.setText("Progresso")
        self.indice_musica_atual = 0
        self.indexOriginal = 0

        self.fimMusica = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.fimMusica)

        self.ui.botaoTocar.clicked.connect(self.playMusic)
        self.ui.botaoEscolher.clicked.connect(self.chooseMusic)
        self.ui.botaoEscolherPasta.clicked.connect(self.chooseMusicFromFolder)
        self.ui.botaoPular.clicked.connect(self.skipMusic)
        self.ui.botaoAnterior.clicked.connect(self.previousMusic)
        self.ui.botaoBaixar.clicked.connect(self.searchMusic)
        self.ui.botaoDownloadFolder.clicked.connect(self.loadDownloadFolder)
        self.ui.botaoEmbaralhar.clicked.connect(self.embaralharMusicas)

        self.menuItens = QMenu(self)

        estiloMenu = """
        QMenu {
            background-color: #800080;
            color: white; 
            border-radius: 5px;
        }

        QMenu::item {
            padding: 5px 15px;
        }

        QMenu::item:selected {
            background-color: #4169E1;
        }
        """
        self.menuItens.setStyleSheet(estiloMenu)

        renomearAcao = QAction("Renomear", self)
        deletarAcao = QAction("Deletar", self)
        self.menuItens.addAction(renomearAcao)
        self.menuItens.addAction(deletarAcao)

        self.ui.listWidget.setContextMenuPolicy(3)
        self.ui.listWidget.customContextMenuRequested.connect(
            self.mostrarMenuItens)

        deletarAcao.triggered.connect(self.removerItem)
        renomearAcao.triggered.connect(self.renomearItem)

        self.download_thread = DownloadThread(
            self.downloadLista)
        self.download_thread.progressoSignal.connect(self.mostrarProgresso)
        self.download_thread.updateDownloadSignal.connect(
            self.updateDownloadList)

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

        self.ui.volumeSlider.valueChanged.connect(self.updateVolume)

        self.timerCaixaDeTexto = QtCore.QTimer(self)
        self.timerCaixaDeTexto.timeout.connect(
            lambda: self.musicasNaoCarregadasHandler(self.musicasNaoCarregadas))
        self.timerCaixaDeTexto.setSingleShot(True)

        self.loadPlaylist()
        self.loadFolders()

    def iniciarTimerFimDownload(self):
        self.timer.start(5000)

    def musicasNaoCarregadasHandler(self, musicasNaoCarregadas):
        msg = "As seguintes músicas não puderam ser carregadas:\n\n"
        msg += "\n".join(musicasNaoCarregadas)

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Músicas não carregadas")
        msg_box.setText(msg)
        msg_box.exec_()

    def renomearItem(self):
        item = self.ui.listWidget.currentItem()
        if item is not None:
            row = self.ui.listWidget.row(item)
            dialog = CaixaDeDialogo("Renomear", "Digite o novo nome")
            if dialog.exec_() == QDialog.Accepted:
                new_name = dialog.input.text()
                if new_name:
                    self.playlist[row]['nome_musica'] = new_name
                    item.setText(new_name)

        self.updateSlider()
        self.updatePlaylistLabel()

    def removerItem(self):
        item = self.ui.listWidget.currentItem()
        if item is not None:
            row = self.ui.listWidget.row(item)
            self.playlist.pop(row)
            self.ui.listWidget.takeItem(row)
            if row < self.indice_musica_atual:
                self.indice_musica_atual -= 1
        self.updatePlaylistLabel()
        self.updateSlider()

    def mostrarMenuItens(self, position):
        self.ui.listWidget.clearFocus()
        acao = self.menuItens.exec_(self.ui.listWidget.mapToGlobal(position))

        if acao is None:
            self.updatePlaylistLabel()

    def updateVolume(self):
        volume = self.ui.volumeSlider.value() / 100.0
        pygame.mixer.music.set_volume(volume)

    def savePlaylist(self):
        data = {
            "playlist": self.playlist,
            "indice_musica_atual": self.indice_musica_atual
        }

        with open('playlist.json', 'w') as file:
            json.dump(data, file, indent=1)

    def saveFolders(self):
        data = {
            "folders": {
                "folderDownload": self.download_thread.downloadFolder
            }
        }

        with open('folders.json', 'w') as file:
            json.dump(data, file, indent=1)

    def loadPlaylist(self):

        volume = self.ui.volumeSlider.value() / 100.0
        pygame.mixer.music.set_volume(volume)

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

            self.indice_musica_atual = data.get('indice_musica_atual', 0)

            if self.musicasNaoCarregadas:
                self.timerCaixaDeTexto.start(500)

            self.playlist = updated_playlist
            self.updatePlaylistLabel()

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def loadFolders(self):
        try:
            with open('folders.json', 'r') as file:
                data = json.load(file)

            self.download_thread.downloadFolder = data['folders']['folderDownload']

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def loadDownloadFolder(self):
        self.download_thread.downloadFolder = escolherPastaDownload(
            self.download_thread.downloadFolder)
        self.saveFolders()

    def mostrarProgresso(self, message):
        self.ui.progressoLabel.setText(message)

    def clicked(self, item):
        self.indexOriginal = self.ui.listWidget.row(item)

    def customDropEvent(self, event):
        drop_position = event.pos()
        dropped_item = self.ui.listWidget.itemAt(drop_position)

        if dropped_item:
            original_index = self.playlist.index(
                self.playlist[self.indexOriginal])
            dropped_index = self.ui.listWidget.row(dropped_item)

            if self.indice_musica_atual == original_index:
                self.indice_musica_atual = dropped_index

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

        for event in pygame.event.get():
            if event.type == self.fimMusica:
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

    def embaralharMusicas(self):
        random.shuffle(self.playlist)
        self.indice_musica_atual = 0
        self.updatePlaylistLabel()

        next_music_path = self.playlist[self.indice_musica_atual]['path']
        pygame.mixer.music.load(next_music_path)
        self.ui.musicaSlider.setValue(0)
        self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
            self.playlist[self.indice_musica_atual]['path']).get_length()))
        self.ui.musicaTocando.setText(
            self.playlist[self.indice_musica_atual]['nome_musica'])
        pygame.mixer.music.play()

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

    def updateDownloadList(self):
        self.ui.downloadList.clear()
        for musica in self.downloadLista:
            if musica not in [self.ui.downloadList.item(i).text() for i in range(self.ui.downloadList.count())]:
                self.ui.downloadList.addItem(musica)

    def updatePlaylistLabel(self):
        self.ui.listWidget.clear()

        for index, item in enumerate(self.playlist):
            music_name = item['nome_musica']
            self.ui.listWidget.addItem(f"{index + 1}. {music_name}")

        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setSelected(i == self.indice_musica_atual)

    def downloadMusic(self):
        if not self.download_thread.isRunning():
            self.ui.progressoLabel.setText("Iniciando download...")
            self.download_thread.start()

    def searchMusic(self):
        caixa = CaixaDeDialogo(
            "Digite o termo de pesquisa", "Digite o nome ou o link:")

        if caixa.exec_() == QDialog.Accepted:
            termoPesquisa = caixa.input.text()
            self.downloadLista.append(termoPesquisa)
            self.updateDownloadList()
            self.downloadMusic()

    def chooseMusic(self):
        self.playlist = escolherMusica(self.playlist)
        self.updatePlaylistLabel()
        self.savePlaylist()

    def chooseMusicFromFolder(self):
        self.playlist = escolherPasta(self.playlist)
        self.updatePlaylistLabel()
        self.savePlaylist()


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()

    app = QtWidgets.QApplication([])

    window = SuaJanelaPrincipal()
    window.show()

    app.aboutToQuit.connect(window.savePlaylist)
    app.aboutToQuit.connect(window.saveFolders)

    app.exec()

    window.download_thread.wait()
    pygame.quit()
