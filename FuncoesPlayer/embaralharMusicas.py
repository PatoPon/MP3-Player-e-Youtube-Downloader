import random, pygame

from .play import playMusic
from .atualizarSelecionado import atualizarSelecionado
from FuncoesLabelPlaylist.updatePlaylistLabel import updatePlaylistLabel

def embaralharMusicas(playlist, indice, musicaSlider, botao, musicaTocando, listWidget):
    pygame.mixer.music.stop()
    random.shuffle(playlist)
    playMusic(playlist, indice, musicaSlider, botao, musicaTocando, listWidget)
    atualizarSelecionado(indice, listWidget)
    updatePlaylistLabel(playlist, indice, listWidget, musicaTocando)
    return playlist