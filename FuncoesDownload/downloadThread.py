from PyQt5.QtCore import QThread, pyqtSignal
import yt_dlp
import os

class DownloadThread(QThread):
    progressoSignal = pyqtSignal(str)
    updateDownloadSignal = pyqtSignal(int)
    updateDownloadFolderSignal = pyqtSignal(str)

    def __init__(self, downloadLista, parent=None):
        super().__init__(parent)
        self.downloadFolder = "../Músicas"
        self.downloadLista = downloadLista

    def run(self):
        while self.downloadLista:
            musica = self.downloadLista[0]
            self.progressoSignal.emit(f"Pesquisando {musica}")

            def progress_callback(status):
                match status['status']:
                    case 'downloading':
                        self.progressoSignal.emit(f"Baixando {musica}")
                        if 'downloaded_bytes' in status and 'total_bytes' in status:
                            downloaded = status['downloaded_bytes']
                            total = status['total_bytes']

                            if total > 0:
                                percentual = int((downloaded / total) * 100)
                                self.progressoSignal.emit(
                                    f"Baixando {musica} ({percentual}%)")

                    case 'finished':
                        self.progressoSignal.emit(f"Convertendo {musica}")
                    case _:
                        self.progressoSignal.emit(f"Processando {musica}")

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'default_search': 'ytsearch',
                'writethumbnail': True,
                'embedthumbnail': True,
                'convert_thumbnails': 'jpg',
                'progress_hooks': [(lambda status: progress_callback(status))],
                'outtmpl': self.downloadFolder+'/%(title)s.%(ext)s',
                'postprocessors': [
                    {
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    },
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                    {
                        "key": "EmbedThumbnail",
                    },
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(musica, download=False)
                if info_dict.get('entries'):
                    if 'extractor' in info_dict and info_dict['extractor'] == 'youtube:playlist':
                        self.progressoSignal.emit(
                            f"Playlists não são suportadas: {musica}")
                    else:
                        musica = info_dict['entries'][0]['title']
                        self.downloadLista[0] = musica
                        self.updateDownloadSignal.emit(self)

                webmNome = ydl.prepare_filename(info_dict)

                ydl.download([musica])

                if not os.path.exists(webmNome):
                    self.progressoSignal.emit(f"{musica}.mp3 foi baixado!")
                    self.downloadLista.remove(musica)
                    self.updateDownloadSignal.emit(self)

        self.progressoSignal.emit("Todas as músicas foram baixadas!")