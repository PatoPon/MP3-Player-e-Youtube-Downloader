import json, os

from FuncoesLabelPlaylist.updatePlaylistLabel import updatePlaylistLabel
from FuncoesDownload.downloadThread import DownloadThread

from Interface.escolherPastas import escolherPastaDownload

def loadPlaylist(playlist, indice, listWidget, musicaLabel, musicasNaoCarregadas, timerCaixaDeTexto, musicaTocando):
    try:
        with open('Dados\\JSON\\playlist.json', 'r') as file:
            data = json.load(file)

        playlist = data.get('playlist', [])
        updated_playlist = []

        for item in playlist:
            try:
                if os.path.exists(item['path']):
                    updated_playlist.append(item)
                else:
                    musicasNaoCarregadas.append(item['nome_musica'])
            except Exception as e:
                musicasNaoCarregadas.append(item['nome_musica'])

        indice = data.get('indice_musica_atual', 0)

        if musicasNaoCarregadas:
            timerCaixaDeTexto.start(500)

        playlist = updated_playlist

        if playlist:
            musicaTocando.setText(
                playlist[indice]["nome_musica"])

        updatePlaylistLabel(playlist, indice, listWidget, musicaLabel)

        return playlist, indice

    except (FileNotFoundError, json.JSONDecodeError):
        return [], 0

def loadFolders():
    try:
        with open('Dados\\JSON\\folders.json', 'r') as file:
            data = json.load(file)

        DownloadThread.downloadFolder = data['folders']['folderDownload']

    except (FileNotFoundError, json.JSONDecodeError):
        return []

def loadDownloadFolder():
    DownloadThread.downloadFolder = escolherPastaDownload(
        DownloadThread.downloadFolder)