import pygame

from .atualizarSelecionado import atualizarSelecionado
from .play import playMusic

def startMusicFromClick(playlist, indice, item, botao, musicaTocando, musicaSlider, listWidget):
    pygame.mixer.music.stop()
    listWidget.clearFocus()
    atualizarSelecionado(indice, listWidget)

    if item < len(playlist):
        indice = item
        playMusic(playlist, indice, musicaSlider, botao, musicaTocando, listWidget)

    return indice