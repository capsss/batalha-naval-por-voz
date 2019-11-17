#bibliotecas necessarias
# pip3 install SpeechRecognition 
# pip3 install pyaudio 
# pip3 install Selenium 
# pip3 install gTTS 

#pra rodar
# python3 battleship.py



#coisas para fazer:
#
#FAZER  -   implementar a fase de posicionamento das pecas (atualmente esta indo com posicionamento aleatorio)
#PRONTO -   estabelecer uma especie de timeout pra entrada de voz, tem hora que demora de mais. era melhor reiniciar o microfone e pedir pra falar de novo
#PRONTO -   trocar os prints por saidas de audio pra fazer mais sentido com a coisa toda
#PRONTO -   implementar uma opção por voz para "jogar de novo", pra nao precisa executar o codigo na mao outra vez
#FAZER  -   pedir pro usuario escolher outra posicao caso tenha escolhida alguma invalida
#FAZER  -   verificar o reconhecimento de voz de acordo com o "three alguma coisa" que tem nos slides
#FAZER  -   trocar a reproducao de audio por uma biblioteca melhor, usar o SO pra isso eh lento, pesado, e ainda por cima abre uma puta janela chata por cima
#PRONTO -   implementar um segundo jogador para automatizar a coisa toda



from selenium import webdriver
from selenium.webdriver import ActionChains
import speech_recognition as sr

import threading
import os
import time

#grava texto em audio
def gravar_mensagem_texto_em_audio(mensagem, nome):
    from gtts import gTTS
    tts = gTTS(text=mensagem, lang='pt-br')
    tts.save(nome + '.mp3')

#reproduz audio
def tocar_audio(arquivo):
    os.system(arquivo + '.mp3')

#escuta o audio e retorna o que foi reconhecido
def reconhecer_audio(mensagem_inicial='falai', mensagem_ajuda='nao entendi, fala direito'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(mensagem_inicial)
        # recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, 5, 5)
            entrada_por_audio = recognizer.recognize_google(audio, language='pt-BR')
            print('reconhecido:', entrada_por_audio)
            return entrada_por_audio
        except:
            print(mensagem_ajuda)
    return None

#mapeia o audio reconhecido pelo usuario para coordenadas no tabuleiro
def mapear_coordenadas(audio_reconhecido):
    if " " in audio_reconhecido:
        duas_palavras = audio_reconhecido.split(' ')
        letra = duas_palavras[0][0]
        y = duas_palavras[1]
        try:
            print('numero:', y)
            return [mapear_letra_para_numero(letra), mapear_numero_para_numero(y)]
        except:
            return [None, None]
    else:
        try:
            return [mapear_letra_para_numero(audio_reconhecido[0]), int(audio_reconhecido[1:])]
        except:
            return [None, None]

#mapeia a letra para o respectivo numero. ex: a=1, b=2, c=3...
def mapear_letra_para_numero(letra):
    switcher = {
        'A' : 1,
        'B' : 2,
        'C' : 3,
        'D' : 4,
        'E' : 5,
        'F' : 6,
        'G' : 7,
        'H' : 8,
        'I' : 9,
        'J' : 10,
        'a' : 1,
        'b' : 2,
        'c' : 3,
        'd' : 4,
        'e' : 5,
        'f' : 6,
        'g' : 7,
        'h' : 8,
        'i' : 9,
        'j' : 10
    }
    return switcher.get(letra, None)

#mapeia numero escrito para numero inteiro. ex: 'zero'=0, 'um'=1, 'dois'=2...
def mapear_numero_para_numero(numero):
    print('numero:', numero)
    switcher = {
        'um' : 1,
        'dois' : 2,
        'três' : 3,
        'treis' : 3,
        'tres' : 3,
        't' : 3,
        'quatro' : 4,
        'cinco' : 5,
        'seis' : 6,
        'sete' : 7,
        'oito' : 8,
        'Oi' : 8,
        'oi' : 8,
        'nove' : 9,
        'dez' : 10
    }
    return switcher.get(numero, None)

#isso aqui eh uma gambiarra pra tentar concertar os reconhecimentos cagados da biblioteca
def concertar_cagada(texto_porcamento_reconhecido):
    if texto_porcamento_reconhecido == 'MI 8': #(i, 8)
        return [9, 8]
    if texto_porcamento_reconhecido == 'ben 10': #(b, 10)
        return [2, 10]
    if texto_porcamento_reconhecido == 'assim': #(a, 5)
        return [1, 5]

    if texto_porcamento_reconhecido == 'e 1' or texto_porcamento_reconhecido == 'E 1': #(e, 1)
        return [5, 1]
    if texto_porcamento_reconhecido == 'e 2' or texto_porcamento_reconhecido == 'E 2': #(e, 2)
        return [5, 2]
    if texto_porcamento_reconhecido == 'e 3' or texto_porcamento_reconhecido == 'E 3': #(e, 3)
        return [5, 3]
    if texto_porcamento_reconhecido == 'e 4' or texto_porcamento_reconhecido == 'E 4': #(e, 4)
        return [5, 4]
    if texto_porcamento_reconhecido == 'e 5' or texto_porcamento_reconhecido == 'E 5': #(e, 5)
        return [5, 5]
    if texto_porcamento_reconhecido == 'e 6' or texto_porcamento_reconhecido == 'E 6': #(e, 6)
        return [5, 6]
    if texto_porcamento_reconhecido == 'e 7' or texto_porcamento_reconhecido == 'E 7': #(e, 7)
        return [5, 7]
    if texto_porcamento_reconhecido == 'e 8' or texto_porcamento_reconhecido == 'E 8': #(e, 8)
        return [5, 8]
    if texto_porcamento_reconhecido == 'e 9' or texto_porcamento_reconhecido == 'E 9': #(e, 9)
        return [5, 9]
    if texto_porcamento_reconhecido == 'e 10' or texto_porcamento_reconhecido == 'E 10': #(e, 10)
        return [5, 10]


    return None

#cria o segundo jogador para fazer jogadas automaticas e aleatorias
def segundo_jogador_automatico(url):
    import random

    #define navegador chrome
    navegador = webdriver.Chrome()
    #minimiza o navegador secundario
    navegador.minimize_window()
    #abre no site do jogo
    navegador.get(url)

    #bora comecar
    botao_start = navegador.find_element_by_class_name('battlefield-start-button')
    botao_start.click()

    time.sleep(5)

    lista_da_fase_atual = navegador.find_elements_by_class_name("notification-message")
    estado = "vez do adversario"

    lista_de_coordenadas_ja_jogadas = []

    while(estado == "sua vez" or estado == "vez do adversario"):
        if estado == "sua vez":
            x = random.randint(0,9)
            y = random.randint(0,9)
            if [x, y] not in lista_de_coordenadas_ja_jogadas:
                campo = navegador.find_elements_by_xpath('//div[@data-y="' +str(y) + '"] [@data-x="' +str(x) + '"]')
                campo[1].click()
                lista_de_coordenadas_ja_jogadas.append([x,y])
                time.sleep(1)

        if lista_da_fase_atual[6].is_displayed(): #Oponente disparar em. Por favor, aguarde.
            estado = "vez do adversario"
        elif lista_da_fase_atual[5].is_displayed():
            estado = "sua vez"
        elif lista_da_fase_atual[7].is_displayed():
            estado = "oponente desistiu"
        elif lista_da_fase_atual[8].is_displayed():
            estado = "ganhou"
        elif lista_da_fase_atual[9].is_displayed():
            estado = "perdeu"

    navegador.close()

# gravar_mensagem_texto_em_audio('Bem vindo ao grande e inovador batalha naval. Que original... A qualquer momento diga "repetir" para que eu fale a última instrução novamente. Para desistir, diga "desistir". Para começar, diga "começar".', 'mensagem_inicial')
# gravar_mensagem_texto_em_audio('Iniciando o jogo...', 'inicio_de_jogo')
# gravar_mensagem_texto_em_audio('Diga uma letra e um número para escolher a casa onde quer atirar, por exemplo: "a7", ou "j2".', 'intrucoes')
# gravar_mensagem_texto_em_audio('Sua vez.', 'sua_vez')
# gravar_mensagem_texto_em_audio('E não é que você é bom nesse bagulho mesmo? Parabéns bixo. Ganhou bonito eim', 'vencedor')
# gravar_mensagem_texto_em_audio('Mas é ruim demais mesmo eim, perdeu de lavada!', 'perdedor')
# gravar_mensagem_texto_em_audio('Vixi, o outro cara arregou? Só assim pra você ganhar mesmo...', 'wo')
# gravar_mensagem_texto_em_audio('Tem certeza que você quer arregar. Seu arregãozinho', 'vai_arregar')
# gravar_mensagem_texto_em_audio('Beleza então, arregão', 'arregao')
# gravar_mensagem_texto_em_audio('Sinto que você quer jogar mais uma não é mesmo? Posso começar uma nova partida?', 'reinicio')
# gravar_mensagem_texto_em_audio('Se cuida então', 'despedida')

tocar_audio('mensagem_inicial')
quer_jogar = True
while(quer_jogar):
    while(quer_jogar):
        entrada_por_audio = reconhecer_audio()
        if(entrada_por_audio == 'começar'):
            break
        if(entrada_por_audio == 'inicializar'):
            break
        if(entrada_por_audio == 'iniciar'):
            break
        if(entrada_por_audio == 'vai porra'):
            break

    tocar_audio('inicio_de_jogo')
    estado = "inicio"

    #define navegador chrome
    navegador = webdriver.Chrome()
    #abre no site do jogo
    navegador.get('http://pt.battleship-game.org/')
    #maximiza a tela
    navegador.maximize_window()

    #muda o tipo de jogo para contra amigo - ficar dependendo de alguem pra inciar o jogo eh foda...
    tipo_de_jogo_contra_amigo = navegador.find_element_by_link_text('amigo')
    tipo_de_jogo_contra_amigo.click()
    #muda o jogo para o modo classico - o modo russo (padrao) tem navios de 1x1, vtnc...
    jogo_tipo_classico = navegador.find_element_by_link_text('clássico')
    jogo_tipo_classico.click()

    #descobre a url para o outro jogador entrar no mesmo jogo
    campo_contendo_a_url_para_convidar_outro_jogador = navegador.find_element_by_class_name('battlefield-start-choose_rival-variant-url-input')
    url = campo_contendo_a_url_para_convidar_outro_jogador.get_attribute("data-value")

    #inicia o segundo jogardor que vai fazer jogadas aleatorias
    t = threading.Thread(target=segundo_jogador_automatico, args=(url,))
    t.daemon = True
    t.start()

    #bora comecar
    botao_start = navegador.find_element_by_class_name('battlefield-start-button')
    botao_start.click()

    #eh extremamente importante saber em que fase esta o jogo
    #o controle atualmente eh pela mensagem que o site mostra
    #apesar de funcionar, ta meio porco isso. tentar mudar mais pra frente...
    lista_da_fase_atual = navegador.find_elements_by_class_name("notification-message")

    #enquanto o outro jogador nao clickar pra iniciar tambem...
    while(not lista_da_fase_atual[3].is_displayed()): #O jogo comecou. Seu tiro.
        time.sleep(1)

    tocar_audio('instrucoes')
    estado = "sua vez"

    while(estado == "sua vez" or estado == "vez do adversario"):
        if estado == "sua vez":
            tocar_audio('sua_vez')
            audio_reconhecido = reconhecer_audio()
            if audio_reconhecido != None:
                if audio_reconhecido == 'desistir' or audio_reconhecido == 'abandonar':
                    print('vai arregar?')
                    tocar_audio('vai_arregar')
                    confirmar_desistencia = reconhecer_audio()
                    if confirmar_desistencia == 'sim':
                        estado = "desistiu"
                        tocar_audio('arregao')
                        break
                coordenadas = concertar_cagada(audio_reconhecido)
                if coordenadas == None:
                    coordenadas = mapear_coordenadas(audio_reconhecido)
                print(coordenadas)
                if coordenadas[0] != None and coordenadas[1] != None:
                    campo = navegador.find_elements_by_xpath('//div[@data-y="' +str(coordenadas[1] - 1) + '"] [@data-x="' +str(coordenadas[0] -1) + '"]')
                    campo[1].click()
            else:
                print('nao foi reconhecido')
        time.sleep(1)

        if lista_da_fase_atual[6].is_displayed(): #Oponente disparar em. Por favor, aguarde.
            estado = "vez do adversario"
        elif lista_da_fase_atual[5].is_displayed(): #Seu tiro.
            estado = "sua vez"
        elif lista_da_fase_atual[7].is_displayed():
            estado = "oponente desistiu"
        elif lista_da_fase_atual[8].is_displayed():
            estado = "ganhou"
        elif lista_da_fase_atual[9].is_displayed():
            estado = "perdeu"



    #quando chegar ate aqui quer dizer que acabou
    #se for o ganhador
    if estado == "ganhou":
        print('ganhador')
        tocar_audio('ganhador')
    if estado == "perdeu":
        print('perdedor')
        tocar_audio('perdedor')
    if estado == "oponente desistiu":
        print('ganhou por w.o.')
        tocar_audio('wo')
    time.sleep(5)
    navegador.close()

    tocar_audio('reinicio')
    resposta = reconhecer_audio()
    if resposta != 'sim' and resposta != 'pode':
        quer_jogar = False
        tocar_audio('despedida')





























# #testes para movimentacao das pecas na fase de posicionamento
# botao_posicionar_aleatorio = navegador.find_element_by_class_name('placeships-variant-link')

# verificacao = True
# x=9
# y=9
# while verificacao:
#     campo1 = navegador.find_element_by_xpath('//div[@data-y="' +str(y) + '"] [@data-x="' +str(x) + '"]')
#     campo2 = navegador.find_element_by_xpath('//div[@data-y="' +str(y) + '"] [@data-x="' +str(x-2) + '"]')

#     # mouse = ActionChains(navegador).drag_and_drop(campo1, campo2)
#     mouse = ActionChains(navegador).click_and_hold(campo1).move_to_element(campo2).click()
#     mouse.perform()
#     time.sleep(1)
#     x -= 1
#     print(x)
#     if x == 2:
#         verificacao = False