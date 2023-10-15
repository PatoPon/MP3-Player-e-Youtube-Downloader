from PyQt5.QtWidgets import *
import vlc
import os, re, urllib.parse

def tocarMusica(player, media_list):
    print(media_list)
    player.set_media_list(media_list)
    player.play()

def proximaMusica(player):
    player.next()

def escolherMusica(player, media_list):
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Arquivos de Áudio (*.mp3)")
    file_dialog.setViewMode(QFileDialog.List)
    file_dialog.setFileMode(QFileDialog.ExistingFiles)

    if file_dialog.exec_():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            # Criar uma nova lista de reprodução
            media_list = vlc.MediaList()

            # Adicionar os novos arquivos selecionados à lista de reprodução
            for file_path in selected_files:
                media = vlc.Media(file_path)
                media_list.add_media(media)

            # Substituir a lista de reprodução existente
            player.set_media_list(media_list)

            # Tocar a primeira música da nova lista
            player.play()
    
    return media_list

def pararMusica(player):
    player.pause()

def updateSlide(slide, player, duracao):
    if player.get_media_player().get_media():
        posicao_em_ms = player.get_media_player().get_time()
    else:
        posicao_em_ms = 0

    if posicao_em_ms != -1:
        posicao_em_segundos = posicao_em_ms
        
        if posicao_em_segundos != 0:
            valor_do_slide = posicao_em_segundos / duracao * 100
        else: 
            valor_do_slide = 0
        slide.setValue(int(valor_do_slide))
    else:
        print('A posição de reprodução não está disponível.')

def updatePlayer(slide, player):
    if player.get_media_player().get_media():
        tamanhoMusica = ((player.get_media_player().get_media().get_duration()) / 1000)
    else:
        tamanhoMusica = 0

    updateSlide(slide, player, tamanhoMusica * 1000)

def limpar_nome_musica(nome_musica):
    # Decodificar URL
    nome_musica_decodificado = urllib.parse.unquote(nome_musica)
    
    # Remove a extensão ".mp3"
    nome_musica_sem_extensao = nome_musica_decodificado.rstrip('.mp3')
    
    # Substitui caracteres especiais e espaços em branco por underscores
    nome_musica_formatado = re.sub(r'[^\w\s-]', '', nome_musica_sem_extensao)
    
    return nome_musica_formatado

def updatePlaylist(media_list):
    playlist = []

    for idx in range(media_list.count()):
        media = media_list.item_at_index(idx)
        path = os.path.normpath(media.get_mrl())
        file_name, file_extension = os.path.splitext(os.path.basename(path))
        nome_musica = limpar_nome_musica(file_name)

        info = {
            "posicao": idx + 1,
            "nome_musica": nome_musica
        }
        playlist.append(info)
    
    return playlist
