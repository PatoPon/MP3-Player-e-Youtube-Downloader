import pygame

from FuncoesPlayer.atualizarSelecionado import atualizarSelecionado
from FuncoesPlayer.play import playMusic

def previousMusic(playlist, indice, musicaSlider, botao, musicaTocando, listWidget):
    atualizarSelecionado(indice, listWidget)
    pygame.mixer.music.stop()
    if playlist:
        if indice - 1 >= 0:
            indice -= 1
        else:
            indice = len(playlist) - 1
    else:
        indice = 0
    playMusic(playlist, indice, musicaSlider, botao, musicaTocando, listWidget)
    return indice