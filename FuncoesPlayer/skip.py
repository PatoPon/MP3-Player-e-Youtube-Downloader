from .play import playMusic
from .atualizarSelecionado import atualizarSelecionado
import pygame

def skipMusic(playlist, indice, musicaSlider, botao, musicaTocando, listWidget):
    atualizarSelecionado(indice, listWidget)
    pygame.mixer.music.stop()
    if playlist:
        if indice + 1 < len(playlist):
            indice += 1
        else:
            indice = 0
    else:
        indice = 0

    playMusic(playlist, indice, musicaSlider, botao, musicaTocando, listWidget)
    return indice