import re

def updatePlaylistLabel(playlist, indice, listWidget, musicaLabel):
    listWidget.clear()

    for index, item in enumerate(playlist):
        music_name = item['nome_musica']
        listWidget.addItem(f"{index + 1}. {music_name}")

    for i in range(listWidget.count()):
        item = listWidget.item(i)
        item.setSelected(i == indice)

    if listWidget.item(indice):
        musicaLabel.setText(re.sub(r'^\d+\.\s', '', listWidget.item(indice).text()))