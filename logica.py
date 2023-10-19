from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pygame  # Importe o Pygame
import os, re, urllib.parse

def tocarMusica(playlist):
    if playlist:
        pygame.mixer.music.load(playlist[0]['path'])
        pygame.mixer.music.play()

def adicionarMusicaAPlaylist(playlist, file_path, numero):
    nome_musica = limpar_nome_musica(os.path.basename(file_path))
    playlist.append({'path': file_path, 'nome_musica': nome_musica})

def escolherPasta(playlist):
    # Crie um diálogo de seleção de pasta
    folder_dialog = QFileDialog()
    folder_dialog.setFileMode(QFileDialog.Directory)
    folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

    if folder_dialog.exec_():
        selected_folder = folder_dialog.selectedFiles()
        if selected_folder:
            folder_path = selected_folder[0]

            # Agora, listamos todos os arquivos .mp3 na pasta selecionada
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.lower().endswith(".mp3"):
                        file_path = os.path.join(root, file_name)
                        nome_musica = limpar_nome_musica(os.path.basename(file_path))

                        # Verifique se a música já está na playlist antes de adicioná-la
                        if nome_musica not in (musica['nome_musica'] for musica in playlist):
                            adicionarMusicaAPlaylist(playlist, file_path, len(playlist) + 1)
    
    return playlist

    return playlist

def escolherMusica(playlist):
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Arquivos de Áudio (*.mp3)")
    file_dialog.setViewMode(QFileDialog.List)
    file_dialog.setFileMode(QFileDialog.ExistingFiles)

    if file_dialog.exec_():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            # Crie um conjunto de músicas já existentes na playlist
            musicas_na_playlist = set(musica['nome_musica'] for musica in playlist)
            numero = len(playlist) + 1  # Comece com o próximo número disponível

            for file_path in selected_files:
                nome_musica = limpar_nome_musica(os.path.basename(file_path))
                # Verifique se a música já está na playlist antes de adicioná-la
                if nome_musica not in musicas_na_playlist:
                    adicionarMusicaAPlaylist(playlist, file_path, numero)
                    musicas_na_playlist.add(nome_musica)
                    numero += 1  # Incremente o número para a próxima música
    
    return playlist

def pararMusica():
    pygame.mixer.music.stop()

def limpar_nome_musica(nome_musica):
    nome_musica_decodificado = urllib.parse.unquote(nome_musica)
    nome_musica_sem_extensao = nome_musica_decodificado.rstrip('.mp3')
    
    nome_musica_formatado = re.sub(r'[^\w\s-]', '', nome_musica_sem_extensao)
    
    return nome_musica_formatado