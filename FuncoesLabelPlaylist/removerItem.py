from .updatePlaylistLabel import updatePlaylistLabel

def removerCurrentItem(playlist, indice, musicaLabel, currentItem, listWidget):
        if currentItem is not None:
            row = listWidget.row(currentItem)
            playlist.pop(row)
            listWidget.takeItem(row)
            if row < indice:
                indice -= 1

        updatePlaylistLabel(playlist, indice, listWidget, musicaLabel)