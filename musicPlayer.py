from FuncoesPlayer.play import playMusic
from FuncoesPlayer.skip import skipMusic
from FuncoesPlayer.updateVolume import updateVolume
from FuncoesPlayer.atualizarSelecionado import atualizarSelecionado
from FuncoesPlayer.clickPlay import startMusicFromClick
from FuncoesPlayer.embaralharMusicas import embaralharMusicas
from FuncoesPlayer.back import previousMusic

class MusicPlayer():
    def __init__(self, ui, playlist):
        self.ui = ui
        self.playlist = playlist

    tocarMusica = staticmethod(playMusic)
    tocarMusicaClique = staticmethod(startMusicFromClick)
    pularMusica = staticmethod(skipMusic)
    anteriorMusica = staticmethod(previousMusic)
    embaralharMusicas = staticmethod(embaralharMusicas)
    ajustarVolume = staticmethod(updateVolume)
    atualizarSelecionado = staticmethod(atualizarSelecionado)