import pygame
from PyQt5 import QtGui

def updateUserSlider(musicaSlider, playlist, indice):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        musicaSlider.setMaximum(int(pygame.mixer.Sound(
            playlist[indice]['path']).get_length()))
        position = musicaSlider.value()
        pygame.mixer.music.set_pos(position)
        pygame.mixer.music.unpause()

def updateSlider(botao, musicaSlider, listWidget):
    listWidget.clearFocus()

    if musicaSlider.isSliderDown():
        return

    if pygame.mixer.music.get_busy():
        musicaSlider.setValue(musicaSlider.value() + 1)