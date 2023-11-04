import pygame

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Interface.PyQt5.designApp import Ui_MainWindow
from musicPlayer import MusicPlayer
from FuncoesDownload.downloadThread import DownloadThread

from Interface.escolherPastas import *
from Interface.caixaDeDialogoPersonalizada import CaixaDeDialogo
from Interface.estilosCSS import estiloMenu

from FuncoesLabelPlaylist.updateSlider import updateSlider, updateUserSlider
from FuncoesLabelPlaylist.removerItem import removerCurrentItem
from FuncoesLabelPlaylist.renomearItem import renomearItem
from FuncoesLabelPlaylist.updatePlaylistLabel import updatePlaylistLabel

from Dados.loader import *
from Dados.saver import *


class sinaisMusicas(QObject):
    pronto_signal = pyqtSignal()
    musicasNaoCarregadasSignal = pyqtSignal(list)


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
        self.indice = 0
        self.indexOriginal = 0

        self.timerCaixaDeTexto = QtCore.QTimer(self)
        self.timerCaixaDeTexto.timeout.connect(
            lambda: self.musicasNaoCarregadasHandler(self.musicasNaoCarregadas))
        self.timerCaixaDeTexto.setSingleShot(True)

        self.fimMusica = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.fimMusica)

        self.playlist, self.indice = loadPlaylist(self.playlist, self.indice, self.ui.listWidget, self.ui.musicaTocando,
                                                  self.musicasNaoCarregadas, self.timerCaixaDeTexto, self.ui.musicaTocando)
        loadFolders()

        self.ui.botaoTocar.clicked.connect(
            lambda: MusicPlayer.tocarMusica(self.playlist, self.indice,
                                            self.ui.musicaSlider, self.ui.botaoTocar, self.ui.musicaTocando, self.ui.listWidget))

        self.ui.botaoEscolher.clicked.connect(
            lambda: addMusica(self.playlist, self.indice, self.ui.musicaTocando, self.ui.listWidget))

        self.ui.botaoEscolherPasta.clicked.connect(
            lambda: AddMusicFromFolder(self.playlist, self.indice, self.ui.musicaTocando, self.ui.listWidget))

        self.ui.botaoPular.clicked.connect(
            lambda indice, self=self: (
                setattr(self, 'indice', MusicPlayer.pularMusica(self.playlist, self.indice,
                                                                self.ui.musicaSlider, self.ui.botaoTocar, self.ui.musicaTocando, self.ui.listWidget)),))

        self.ui.botaoAnterior.clicked.connect(
            lambda indice, self=self: (
                setattr(self, 'indice', MusicPlayer.anteriorMusica(self.playlist, self.indice,
                                                                   self.ui.musicaSlider, self.ui.botaoTocar, self.ui.musicaTocando, self.ui.listWidget)),))

        self.ui.botaoBaixar.clicked.connect(self.searchMusic)
        self.ui.botaoDownloadFolder.clicked.connect(loadDownloadFolder)

        self.ui.botaoEmbaralhar.clicked.connect(lambda: (
            setattr(self, 'playlist', MusicPlayer.embaralharMusicas(self.playlist, 0,
                    self.ui.musicaSlider, self.ui.botaoTocar, self.ui.musicaTocando, self.ui.listWidget)),
            setattr(self, 'indice', 0),
        ))

        self.menuItens = QMenu(self)
        self.menuItens.setStyleSheet(estiloMenu)

        renomearAcao = QAction("Renomear", self)
        deletarAcao = QAction("Deletar", self)
        self.menuItens.addAction(renomearAcao)
        self.menuItens.addAction(deletarAcao)

        self.ui.listWidget.setContextMenuPolicy(3)
        self.ui.listWidget.customContextMenuRequested.connect(
            self.mostrarMenuItens)

        deletarAcao.triggered.connect(
            lambda: removerCurrentItem(self.playlist, self.indice, self.ui.musicaTocando,
                                       self.ui.listWidget.currentItem(), self.ui.listWidget))
        renomearAcao.triggered.connect(
            lambda: renomearItem(self.playlist, self.indice, self.ui.musicaTocando,
                                 self.ui.listWidget.currentItem(), self.ui.listWidget))

        self.download_thread = DownloadThread(
            self.downloadLista)
        self.download_thread.progressoSignal.connect(self.mostrarProgresso)
        self.download_thread.updateDownloadSignal.connect(
            self.updateDownloadList)

        self.ui.listWidget.itemClicked.connect(lambda item:
                                               setattr(self, 'indice', MusicPlayer.tocarMusicaClique(self.playlist, self.indice, self.ui.listWidget.row(item),
                                                                                                     self.ui.botaoTocar, self.ui.musicaTocando, self.ui.musicaSlider, self.ui.listWidget)))

        self.ui.listWidget.setDragEnabled(True)
        self.ui.listWidget.setAcceptDrops(True)
        self.ui.listWidget.setDragDropMode(QListWidget.InternalMove)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(
            lambda: self.ui.progressoLabel.setText("Progresso"))
        self.timer.setSingleShot(True)

        self.signals.pronto_signal.connect(lambda: self.timer.start(5000))

        self.timerSlide = QtCore.QTimer(self)
        self.timerSlide.timeout.connect(
            lambda: updateSlider(self.ui.botaoTocar, self.ui.musicaSlider, self.ui.listWidget))
        self.timerSlide.start(1000)

        self.ui.musicaSlider.sliderReleased.connect(
            lambda: updateUserSlider(self.ui.musicaSlider, self.playlist, self.indice))
        self.ui.musicaSlider.setPageStep(0)

        self.ui.listWidget.dropEvent = self.customDropEvento
        self.ui.listWidget.itemPressed.connect(self.clicked)

        self.ui.volumeSlider.valueChanged.connect(
            lambda: MusicPlayer.ajustarVolume(self.ui.volumeSlider))

        volume = self.ui.volumeSlider.value() / 100.0
        pygame.mixer.music.set_volume(volume)

        self.timerEventHandler = QtCore.QTimer(self)
        self.timerEventHandler.timeout.connect(
            self.eventHandler)
        self.timerEventHandler.start(50)

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == self.fimMusica and self.ui.musicaSlider.value() == self.ui.musicaSlider.maximum():
                if self.indice < len(self.playlist) - 1:
                    self.indice += 1
                else:
                    self.indice = 0
                MusicPlayer.tocarMusica(self.playlist, self.indice, self.ui.musicaSlider,
                                        self.ui.botaoTocar, self.ui.musicaTocando, self.ui.listWidget)

    def musicasNaoCarregadasHandler(self, musicasNaoCarregadas):
        msg = "As seguintes músicas não puderam ser carregadas:\n\n"
        msg += "\n".join(musicasNaoCarregadas)

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Músicas não carregadas")
        msg_box.setText(msg)
        msg_box.exec_()

    def mostrarMenuItens(self, position):
        self.ui.listWidget.clearFocus()
        acao = self.menuItens.exec_(self.ui.listWidget.mapToGlobal(position))

        from FuncoesLabelPlaylist.updatePlaylistLabel import updatePlaylistLabel
        updatePlaylistLabel(self.playlist, self.indice,
                            self.ui.listWidget, self.ui.musicaTocando)

    def mostrarProgresso(self, message):
        self.ui.progressoLabel.setText(message)

    def clicked(self, item):
        self.indexOriginal = self.ui.listWidget.row(item)

    def customDropEvento(self, event):
        drop_position = event.pos()
        dropped_item = self.ui.listWidget.itemAt(drop_position)

        if dropped_item:
            dropped_index = self.ui.listWidget.row(dropped_item)

            if dropped_index is not None and 0 <= dropped_index < len(self.playlist):
                nomeMusicaAtual = self.playlist[self.indice]['nome_musica']

                self.playlist.insert(
                    dropped_index, self.playlist.pop(self.indexOriginal))
                    
                for index, item in enumerate(self.playlist):
                    if item['nome_musica'] == nomeMusicaAtual:
                        self.indice = index
                        break

        from FuncoesLabelPlaylist.updatePlaylistLabel import updatePlaylistLabel
        updatePlaylistLabel(self.playlist, self.indice,
                            self.ui.listWidget, self.ui.musicaTocando)

    def updateDownloadList(self):
        self.ui.downloadList.clear()
        for musica in self.downloadLista:
            if musica not in [self.ui.downloadList.item(i).text() for i in range(self.ui.downloadList.count())]:
                self.ui.downloadList.addItem(musica)

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


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()

    app = QtWidgets.QApplication([])

    window = SuaJanelaPrincipal()
    window.show()

    app.aboutToQuit.connect(
        lambda: (print(window.indice), savePlaylist(window.playlist, window.indice)))
    app.aboutToQuit.connect(saveFolders)

    app.exec()

    window.download_thread.wait()
    pygame.quit()
