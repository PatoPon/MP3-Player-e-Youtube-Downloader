import json

from FuncoesDownload.downloadThread import DownloadThread
from FuncoesLabelPlaylist import updatePlaylistLabel

def savePlaylist(playlist, indice):
    data = {
        "playlist": playlist,
        "indice_musica_atual": indice
    }

    with open('Dados\\JSON\\playlist.json', 'w') as file:
        json.dump(data, file, indent=1)

def saveFolders():
    data = {
        "folders": {
            "folderDownload": DownloadThread.downloadFolder
        }
    }

    with open('Dados\\JSON\\folders.json', 'w') as file:
        json.dump(data, file, indent=1)