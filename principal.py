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


class MyListWidget(QListWidget):
    def dropEvent(self, event):
        super().dropEvent(event)
        print("Item solto")


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
        self.indexOriginal = 0

        self.SONG_END = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.SONG_END)

        # Agora você pode interagir com os elementos da interface
        self.ui.botaoTocar.clicked.connect(self.tocarMusica)
        self.ui.botaoEscolher.clicked.connect(self.escolherMusica)
        self.ui.botaoPular.clicked.connect(self.pularMusica)
        self.ui.botaoAnterior.clicked.connect(self.anteriorMusica)
        self.ui.botaoBaixar.clicked.connect(self.procurarMusica)

        self.ui.listWidget.itemClicked.connect(self.iniciarMusicaClicada)

        self.ui.listWidget.setDragEnabled(True)
        self.ui.listWidget.setAcceptDrops(True)
        self.ui.listWidget.setDragDropMode(QListWidget.InternalMove)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.ui.progressoLabel.setText(
            "Progresso"))  # Conecte o slot de redefinição
        self.timer.setSingleShot(True)

        self.signals.pronto_signal.connect(lambda:
                                           self.timer.start(5000)
                                           )

        self.timerSlide = QtCore.QTimer(self)
        self.timerSlide.timeout.connect(self.atualizarSlider)
        self.timerSlide.start(1000)

        self.ui.musicaSlider.sliderReleased.connect(self.atualizarSliderUsuario)

        self.ui.listWidget.dropEvent = self.customDropEvent
        self.ui.listWidget.itemPressed.connect(self.clicked)

    def clicked(self, item):
        self.indexOriginal = self.ui.listWidget.row(item)

    def customDropEvent(self, event):
        drop_position = event.pos()
        # Encontre o item na posição do cursor do mouse
        dropped_item = self.ui.listWidget.itemAt(drop_position)

        if dropped_item:
            # Obtém o índice do item que está sendo arrastado
            original_index = self.playlist.index(
                self.playlist[self.indexOriginal])

            # Obtém o índice do item onde o usuário soltou o item arrastado
            dropped_index = self.ui.listWidget.row(dropped_item)

            if dropped_index is not None and 0 <= dropped_index < len(self.playlist) and original_index != dropped_index:
                # Realiza a troca dos dois itens na lista
                self.playlist[original_index], self.playlist[dropped_index] = self.playlist[dropped_index], self.playlist[original_index]

                # Atualiza a interface ou faça outras operações necessárias
                self.atualizarPlaylistLabel()

    def atualizarSliderUsuario(self):
        print('oi')
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            position = self.ui.musicaSlider.value()
            pygame.mixer.music.set_pos(position)
            pygame.mixer.music.unpause()

    def atualizarSlider(self):
        if pygame.mixer.music.get_busy():
            self.ui.musicaTocando.setText(
                self.playlist[self.indice_musica_atual]['nome_musica'])
            self.ui.musicaSlider.setValue(self.ui.musicaSlider.value() + 1)
        else:
            try:
                self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            except:
                self.ui.musicaTocando.setText("Nenhuma música selecionada")

        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.pularMusica()

    def tocarMusica(self):
        if not pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.unpause()
            elif self.playlist:
                pygame.mixer.music.load(
                    self.playlist[self.indice_musica_atual]['path'])
                self.ui.musicaSlider.setValue(0)
                self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                    self.playlist[self.indice_musica_atual]['path']).get_length()))
                self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
                pygame.mixer.music.play()

                for i in range(self.ui.listWidget.count()):
                    item = self.ui.listWidget.item(i)
                    item.setSelected(i == self.indice_musica_atual)
        else:
            pygame.mixer.music.pause()

    def pularMusica(self):
        if self.playlist:

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
            self.ui.musicaSlider.setValue(0)
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            pygame.mixer.music.play()

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setSelected(i == self.indice_musica_atual)

    def anteriorMusica(self):
        if self.playlist:
            pygame.mixer.music.pause()

            if hasattr(self, 'indice_musica_atual') and self.indice_musica_atual > 0:
                self.indice_musica_atual -= 1
            else:
                self.indice_musica_atual = len(self.playlist) - 1

            musica_anterior_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(musica_anterior_path)
            self.ui.musicaSlider.setValue(0)
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            pygame.mixer.music.play()

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setSelected(i == self.indice_musica_atual)

    def iniciarMusicaClicada(self, item):
        self.ui.listWidget.clearFocus()
        index = self.ui.listWidget.row(item)
        if index < len(self.playlist):
            pygame.mixer.music.pause()
            self.indice_musica_atual = index
            proxima_musica_path = self.playlist[self.indice_musica_atual]['path']
            pygame.mixer.music.load(proxima_musica_path)
            self.ui.musicaSlider.setValue(0)
            self.ui.musicaSlider.setMaximum(int(pygame.mixer.Sound(
                self.playlist[self.indice_musica_atual]['path']).get_length()))
            self.ui.musicaTocando.setText(self.playlist[self.indice_musica_atual]['nome_musica'])
            pygame.mixer.music.play()

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setSelected(i == self.indice_musica_atual)

    def atualizarPlaylistLabel(self):
        self.ui.listWidget.clear()
        for index, item in enumerate(self.playlist):
            nome_musica = item['nome_musica']
            self.ui.listWidget.addItem(f"{index + 1}. {nome_musica}")
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setSelected(i == self.indice_musica_atual)

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
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()  # Inicialize o Pygame
    app = QtWidgets.QApplication([])
    window = SuaJanelaPrincipal()
    window.show()
    app.exec()
    pygame.quit()  # Finalize o Pygame quando a aplicação encerrar
