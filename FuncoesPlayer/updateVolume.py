import pygame

def updateVolume(volumeSlider):
    volume = volumeSlider.value() / 100.0
    pygame.mixer.music.set_volume(volume)