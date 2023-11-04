from PyQt5.QtWidgets import *
import os, re, urllib.parse

from Dados.saver import savePlaylist
from FuncoesLabelPlaylist.updatePlaylistLabel import updatePlaylistLabel

def adicionarMusicaAPlaylist(playlist, file_path):
    nome_musica = limparNome(os.path.basename(file_path))
    playlist.append({'path': file_path, 'nome_musica': nome_musica})

def escolherPasta(playlist):
    folder_dialog = QFileDialog()
    folder_dialog.setFileMode(QFileDialog.Directory)
    folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

    if folder_dialog.exec_():
        selected_folder = folder_dialog.selectedFiles()
        if selected_folder:
            folder_path = selected_folder[0]

            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.lower().endswith(".mp3"):
                        file_path = os.path.join(root, file_name)
                        file_path = os.path.normpath(file_path)
                        if file_path not in {musica['path'] for musica in playlist}:
                            adicionarMusicaAPlaylist(playlist, file_path)
    
    return playlist

def escolherPastaDownload(downloadFolder):
    folder_dialog = QFileDialog()
    folder_dialog.setFileMode(QFileDialog.Directory)
    folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

    if folder_dialog.exec_():
        selected_folder = folder_dialog.selectedFiles()
        if selected_folder:
            folder_path = selected_folder[0]
            return folder_path
    
    return downloadFolder

def escolherMusica(playlist):
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Arquivos de Áudio (*.mp3)")
    file_dialog.setViewMode(QFileDialog.List)
    file_dialog.setFileMode(QFileDialog.ExistingFiles)

    if file_dialog.exec_():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            musicas_na_playlist = {musica['path'] for musica in playlist}

            for file_path in selected_files:
                file_path = os.path.normpath(file_path)
                if file_path not in musicas_na_playlist:
                    adicionarMusicaAPlaylist(playlist, file_path)
                    musicas_na_playlist.add(file_path)
    
    return playlist

def addMusica(playlist, indice, musicaTocando, listWidget):
    playlist = escolherMusica(playlist)
    updatePlaylistLabel(playlist, indice, listWidget, musicaTocando)
    savePlaylist(playlist, indice)

def AddMusicFromFolder(playlist, indice, musicaTocando, listWidget):
    playlist = escolherPasta(playlist)
    updatePlaylistLabel(playlist, indice, listWidget, musicaTocando)
    savePlaylist(playlist, indice)

def limparNome(nomeMusica):
    nomeMusicaDecodificado = urllib.parse.unquote(nomeMusica)
    nomeMusicaSemExtensao = nomeMusicaDecodificado.rstrip('.mp3')
    
    nomeMusicaFormatado = re.sub(r'[^\w\s-]', '', nomeMusicaSemExtensao)
    
    return nomeMusicaFormatado