from Interface.caixaDeDialogoPersonalizada import CaixaDeDialogo
from PyQt5.QtWidgets import QDialog

from .updatePlaylistLabel import updatePlaylistLabel

def renomearItem(playlist, indice, musicaLabel, currentItem, listWidget):
        if currentItem is not None:
            row = listWidget.row(currentItem)
            nomeMusica = playlist[row]['nome_musica']
            dialog = CaixaDeDialogo("Renomear", "Digite o novo nome")
            dialog.input.setText(nomeMusica)
            if dialog.exec_() == QDialog.Accepted:
                new_name = dialog.input.text()
                if new_name:
                    playlist[row]['nome_musica'] = new_name
                    currentItem.setText(new_name)

        updatePlaylistLabel(playlist, indice, listWidget, musicaLabel)