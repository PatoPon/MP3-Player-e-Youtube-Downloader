import pygame
from PyQt5 import QtGui

from .atualizarSelecionado import atualizarSelecionado

def playMusic(playlist, indice, musicaSlider, botao, musicaTocando, listWidget):
    atualizarSelecionado(indice, listWidget)
    if not pygame.mixer.music.get_busy():
        botao.setIcon(QtGui.QIcon('Imagens\\parar.png'))
        if pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.unpause()
        elif playlist:
            pygame.mixer.music.load(
                playlist[indice]['path'])
            musicaSlider.setValue(0)
            musicaSlider.setMaximum(int(pygame.mixer.Sound(
                playlist[indice]['path']).get_length()))
            musicaTocando.setText(
                playlist[indice]['nome_musica'])
            pygame.mixer.music.play()
    else:
        botao.setIcon(QtGui.QIcon('Imagens\\reproduzir.png'))
        pygame.mixer.music.pause()