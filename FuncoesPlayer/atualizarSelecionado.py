def atualizarSelecionado(indice, listWidget):
    for i in range(listWidget.count()):
        item = listWidget.item(i)
        item.setSelected(i == indice)