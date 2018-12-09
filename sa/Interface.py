#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from copy import deepcopy
from time import sleep
from tkinter import *
from random import randint
from SA.mensagens_auditor import *
from SA import compartilhados
from SA.coordenada import *

class InterfaceGrafica:

    def __init__(self, status):
        compartilhados.init()
        self.status = status
        inicia = Tk()
        inicia.title("Bem vindo")
        self.fontePadrao = ("Arial", "40")
        self.fonteMenor = ("Arial", "30")
        self.fonteMapa = ('Helvetica 12 bold')
        self.backgroudDefault = "gray75"

        self.container8 = Frame(inicia)
        self.container9 = Frame(inicia)
        self.container10 = Frame(inicia)
        self.container11 = Frame(inicia)

        self.container8.pack()
        self.container9.pack()
        self.container10.pack()
        self.container11.pack()

        inicia.geometry("1000x700")

        self.container8["pady"] = 30
        self.container9["padx"] = 10
        self.container10["padx"] = 10

        self.titulo = Label(self.container8, text='Escolha uma das opções abaixo', font=self.fontePadrao,pady="25").pack()
        self.espaco = Label(self.container8, text='', font=self.fontePadrao, pady="25").pack()
        self.b1 = Button(self.container9, text='Cadastrar robô', font=self.fonteMenor, command=self.cadastro,bg=self.backgroudDefault, width=20).pack()
        self.b2 = Button(self.container10, text='Novo Jogo', font=self.fonteMenor, command=self.novoJogo, bg=self.backgroudDefault, width=20).pack()

        inicia.mainloop()

    def cadastro(self):
        self.cadastro = Tk()
        self.cadastro.title("Cadastro")
        self.fontePadrao = ("Arial", "40")
        self.fonteMenor = ("Arial", "30")
        self.fonteMapa = ('Helvetica 12 bold')
        self.backgroudDefault = "gray75"

        # ------------- DADOS -------------
        # self.nomeR1 = ""
        # self.nomeR2 = ""

        self.container12 = Frame(self.cadastro)
        self.container13 = Frame(self.cadastro)
        self.container14 = Frame(self.cadastro)
        self.container15 = Frame(self.cadastro)
        self.container16 = Frame(self.cadastro)

        # adicionando os containers
        self.container12.pack()
        self.container13.pack()
        self.container14.pack()
        self.container15.pack()
        self.container16.pack()

        # ---------- MAPA ----------
        self.cadastro.geometry("1000x700")
        # mapa.configure(background="Gray")

        # --------------------- DADOS CADASTRAIS DE CADA ROBÔ ---------------------

        self.container13["pady"] = 10
        self.container14["padx"] = 20
        self.container15["padx"] = 20
        self.container16["padx"] = 20

        self.espaco = Label(self.container12, text='', pady="25").pack()
        self.titulo = Label(self.container12, text='Cadastro', font=self.fontePadrao, pady="25").pack()
        self.espaco = Label(self.container12, text='', pady="25").pack()

        self.nomeLabel = Label(self.container13, text="Nome", font=self.fonteMenor)
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.container13)
        self.nome["width"] = 20
        self.nome["font"] = self.fonteMenor
        self.nome.pack(side=LEFT)

        self.corLabel = Label(self.container14, text="Cor", font=self.fonteMenor)
        self.corLabel.pack(side=LEFT)
        self.cor = Entry(self.container14)
        self.cor["width"] = 20
        self.cor["font"] = self.fonteMenor
        self.cor.pack(side=LEFT)

        self.macLabel = Label(self.container15, text="MAC", font=self.fonteMenor)
        self.macLabel.pack(side=LEFT)

        self.mac = Entry(self.container15)
        self.mac["width"] = 20
        self.mac["font"] = self.fonteMenor
        self.mac.pack(side=LEFT)

        self.autenticar = Button(self.container16)
        self.autenticar["text"] = "Autenticar"
        self.autenticar["font"] = self.fonteMenor
        self.autenticar["width"] = 12
        self.autenticar['bg'] = 'chartreuse3'
        self.autenticar["command"] = self.validaCadastro
        self.autenticar.pack()

        self.espaco = Label(self.container16, text='', pady="10").pack()
        self.mensagem = Label(self.container16, text="", font=self.fonteMenor)
        self.mensagem.pack()

        self.cadastro.mainloop()

    def validaCadastro(self):
        robo = self.nome.get()
        cor = self.cor.get() #TODO VER SE A COR ESCOLHIDA REALMENTE EXISTE, OU SE JÁ NÃO FOI ESCOLHIDA
        mac = self.mac.get() #TODO TEM COMO VERIFICAR SE O MAC É VÁLIDO?

        # TODO validação das informações
        # TODO TRATAR ANTES DE ENVIAR PARA O BANCO DE DADOS

        msg = {'_robo': robo, 'cor': cor, 'mac': mac, '_dir': 'ui'}
        self.avisar_gerenciador(msg)
        self.mensagem['foreground'] = 'darkgreen'
        self.mensagem["text"] = "Cadastrado com sucesso"
        self.nome.delete(0, END)
        self.cor.delete(0, END)
        self.mac.delete(0, END)
        #sleep(1) # TODO mensagem não aparece
        #self.cadastro.destroy()

    def novoJogo(self):
        novoJogo = Tk()
        novoJogo.title("Novo Jogo")
        self.fontePadrao = ("Arial", "40")
        self.fonteMenor = ("Arial", "30")
        self.fonteMapa = ('Helvetica 12 bold')
        self.backgroudDefault = "gray75"

        # ------------- DADOS -------------
        # self.nomeR1 = ""
        # self.nomeR2 = ""

        self.container12 = Frame(novoJogo)
        self.container13 = Frame(novoJogo)
        self.container14 = Frame(novoJogo)
        self.container15 = Frame(novoJogo)
        self.container16 = Frame(novoJogo)
        self.container17 = Frame(novoJogo)
        self.container18 = Frame(novoJogo)
        self.container19 = Frame(novoJogo)
        self.container20 = Frame(novoJogo)
        self.container21 = Frame(novoJogo)
        self.container22 = Frame(novoJogo)
        self.container23 = Frame(novoJogo)

        # adicionando os containers
        self.container12.pack()
        self.container13.pack()
        self.container14.pack()
        self.container15.pack()
        self.container16.pack()
        self.container17.pack()
        self.container18.pack()
        self.container19.pack()
        self.container20.pack()
        self.container21.pack()
        self.container22.pack()
        self.container23.pack()

        novoJogo.geometry("1000x700")

        self.container13["pady"] = 10
        self.container14["padx"] = 20
        self.container15["padx"] = 20
        self.container16["padx"] = 20

        self.titulo = Label(self.container12, text='Novo Jogo', font=self.fontePadrao, pady="10").pack()

        self.modoJogoLabel1 = Label(self.container13, text="Modo de jogo", font=self.fonteMenor)
        self.modoJogoLabel1.pack(side=LEFT)

        self.modoJogo = Entry(self.container13)
        self.modoJogo["width"] = 5
        self.modoJogo["font"] = self.fonteMenor
        self.modoJogo.pack(side=LEFT)

        self.subTitulo = Label(self.container14, text='--- Robô 1 ---', font=self.fonteMenor, pady="25").pack()

        self.nomeLabel1 = Label(self.container15, text="Nome", font=self.fonteMenor)
        self.nomeLabel1.pack(side=LEFT)

        self.nome1 = Entry(self.container15)
        self.nome1["width"] = 15
        self.nome1["font"] = self.fonteMenor
        self.nome1.pack(side=LEFT)

        self.x1Label = Label(self.container16, text="x", font=self.fonteMenor)
        self.x1Label.pack(side=LEFT)

        self.x1 = Entry(self.container16)
        self.x1["width"] = 5
        self.x1["font"] = self.fonteMenor
        self.x1.pack(side=LEFT)

        self.y1Label = Label(self.container16, text="y", font=self.fonteMenor)
        self.y1Label.pack(side=LEFT)

        self.y1 = Entry(self.container16)
        self.y1["width"] = 5
        self.y1["font"] = self.fonteMenor
        self.y1.pack(side=RIGHT)

        self.subTitulo = Label(self.container17, text='--- Robô 2 ---', font=self.fonteMenor,
                            pady="25").pack()

        self.nomeLabel2 = Label(self.container18, text="Nome", font=self.fonteMenor)
        self.nomeLabel2.pack(side=LEFT)

        self.nome2 = Entry(self.container18)
        self.nome2["width"] = 15
        self.nome2["font"] = self.fonteMenor
        self.nome2.pack(side=LEFT)

        self.x2Label = Label(self.container19, text="x", font=self.fonteMenor)
        self.x2Label.pack(side=LEFT)

        self.x2 = Entry(self.container19)
        self.x2["width"] = 5
        self.x2["font"] = self.fonteMenor
        self.x2.pack(side=LEFT)

        self.y2Label = Label(self.container19, text="y", font=self.fonteMenor)
        self.y2Label.pack(side=LEFT)

        self.y2 = Entry(self.container19)
        self.y2["width"] = 5
        self.y2["font"] = self.fonteMenor
        self.y2.pack(side=RIGHT)

        self.espaco = Label(self.container20, text='', pady="10").pack()

        self.autenticar = Button(self.container21)
        self.autenticar["text"] = "Autenticar"
        # self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["font"] = self.fonteMenor
        self.autenticar["width"] = 12
        self.autenticar['bg'] = 'chartreuse3'
        self.autenticar["command"] = self.validaPartida
        self.autenticar.pack()

        self.mensagem = Label(self.container21, text="", font=self.fonteMenor)
        self.mensagem.pack()

        novoJogo.mainloop()

    def validaPartida(self):
        self.modo = self.modoJogo.get()
        self.robo1 = self.nome1.get()
        self.robo2 = self.nome2.get()
        self.posX1 = int(self.x1.get())
        self.posY1 = int(self.y1.get())
        self.posX2 = int(self.x2.get())
        self.posY2 = int(self.y2.get())

        # TODO validação das informações
        # TODO TRATAR ANTES DE ENVIAR PARA O BANCO DE DADOS

        self.cacas = []

        # Sorteia cacas
        for i in range(0, 5):
            caca = {}
            caca["x"] = randint(1, 5)
            caca["y"] = randint(1, 5)
            self.cacas.append(caca)

        msg = {'_robo': '', "cmd": MsgUItoAuditor.NovoJogo, "modo_jogo": self.modo, "cacas": self.cacas, 'jogadorA': self.robo1, 'xA': self.posX1, 'yA': self.posY1, 'jogadorB': self.robo2, 'xB': self.posX2, 'yB': self.posY2, '_dir': 'ui'}

        self.status.definirPartida(self.robo1, self.posX1, self.posY1, self.robo2, self.posY1, self.posY2, self.cacas)

        self.avisar_gerenciador(msg)
        self.mensagem['foreground'] = 'darkgreen'
        self.mensagem["text"] = "Partida pronta"

        # Tratar se estiver nulo
        self.modoJogo.delete(0, END)
        self.nome1.delete(0, END)
        self.nome2.delete(0, END)
        self.x1.delete(0, END)
        self.y1.delete(0, END)
        self.x2.delete(0, END)
        self.y2.delete(0, END)
        # sleep(1) # TODO mensagem não aparece

        # inicia partida
        self.partida()

    def partida(self):
        dados = Tk()
        mapa = Tk()
        dados.title("Informações")
        mapa.title("Mapa")
        self.fontePadrao = ("Arial", "40")
        self.fonteMenor = ("Arial", "30")
        self.fonteMapa = ('Helvetica 12 bold')
        self.backgroudDefault = "gray75"

        # ------------- DADOS -------------
        # self.nomeR1 = ""
        # self.nomeR2 = ""
        # self.cacas1 = 0
        # self.cacas2 = 0
        self.textoParadaR1 = StringVar()  # texto "Parada de emergência"
        self.textoParadaR2 = StringVar()
        self.dadosR1 = StringVar()  # qtd cacas encontradas, pos atual e prox pos
        self.dadosR2 = StringVar()
        self.dadosGerais = StringVar()  # total cacas, cacas encontradas e cacas restantes
        self.textoPausa = StringVar()  # escreve pausa ou continua, dependendo da status do robô

        # ----- OBTENDO INFORMAÇÕES DO BANCO DE DADOS -----
        # self.gerente_db = GerenteDB()
        # self.partidas = self.gerente_db.get_partidas()
        # self.cadastros = self.gerente_db.get_partidas()

        # for partida in self.partidas:
        #     # print(cadastro.get('nome'))
        #     self.nomeR1 = partida.get('robo_a')
        #     self.nomeR2 = partida.get('robo_b')

        # i = 0
        # for cadastro in self.cadastros:
        #     self.backgroud[i] = cadastro.get('cor')
        #     i = i + 1

        # --- Cor dos LEDs dos robôs ----
        self.backgroudR1 = "red2"
        self.backgroudR2 = "gold"

        # --- Cor das coordenadas (0,0) e (20,20) -----
        self.backgroudMapa00 = "yellow"
        self.backgroudMapa66 = "blue"

        self.container1 = Frame(mapa)
        self.container2 = Frame(dados)
        self.container3 = Frame(dados)
        self.container4 = Frame(dados)
        self.container5 = Frame(dados)
        self.container6 = Frame(dados)
        self.container7 = Frame(mapa)

        # adicionando os containers
        self.container1.pack()
        self.container2.pack()
        self.container3.pack()
        self.container4.pack()
        self.container5.pack()
        self.container6.pack()
        self.container7.pack()

        # ---------- MAPA ----------
        mapa.geometry("1000x700")
        # mapa.configure(background="Gray")

        self.espaco = Label(self.container1, text='Mapa', font=self.fontePadrao, pady="50").pack()

        # self.desenhaMapa("G1", 0, 7, "G2", 6,1)

        self.R1 = Coordenada(self.posX1, self.posY1)
        self.R1 = self.transformaCoord(self.R1)

        self.R2 = Coordenada(self.posX2, self.posY2)
        self.R2 = self.transformaCoord(self.R2)

        self.desenhaMapa()
        self.desenhaInfo()

        dados.mainloop()
        mapa.mainloop()

        self.atualizaPartida()

    def desenhaMapa(self):

        #print("(%d, %d)" % (listaCacas[0].getX(), listaCacas[0].getY()))
        #print("R1 (%d, %d)" % (posR1.getX(), posR1.getY()))

        for i in range(0, 8):
            for j in range(0, 8):

                self.b1 = Button(self.container7, padx=20, pady=10, width=2)
                self.b1.grid(row=i, column=j, sticky='news', padx=5, pady=5)

                if (i == 7 and j == 0): # Espaço vazio entre 0 e 0
                    self.coord = Label(self.container7, text='')
                    self.coord.grid(row=i, column=j, sticky='news')

                if (i == 7 and j != 0): # Eixo X do tabuleiro
                    self.coord = Label(self.container7, text='%d' % (j - 1))
                    self.coord.grid(row=i, column=j, sticky='news')

                if (j == 0 and i != 7): # Eixo Y do tabuleiro
                    self.coord = Label(self.container7, text='%d' % (abs(i - 6)))
                    self.coord.grid(row=i, column=j, sticky='news')

                if (i == 6 and j == 1):  # Extremo inferior

                    self.b1 = Button(self.container7, padx=20, pady=10)
                    self.b1.grid(row=i, column=j, sticky='news', padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa00)

                elif (i == 0 and j == 7): # Extremo superior
                    self.b1 = Button(self.container7, padx=20, pady=10)
                    self.b1.grid(row=i, column=j, sticky='news', padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa66)

                # Desenha posição do robô 1
                xR1 = self.R1.getX()
                yR1 = self.R1.getY()
                if (xR1 == 6 and yR1 == 1):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=self.robo1, font=self.fonteMapa)
                    self.b1.grid(row=xR1, column=yR1, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa00, bg=self.backgroudR1)

                elif (xR1 == 0 and yR1 == 7):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=self.robo1)
                    self.b1.grid(row=xR1, column=yR1, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa66, bg=self.backgroudR1,font=self.fonteMapa)

                else:
                    self.b1 = Button(self.container7, padx=20, pady=10, text=self.robo1, font=self.fonteMapa)
                    self.b1.grid(row=xR1, column=yR1, padx=5, pady=5)
                    self.b1.config(bg=self.backgroudR1)

                # Desenha posição do robô 2
                xR2 = self.R2.getX()
                yR2 = self.R2.getY()
                if (xR2 == 6 and yR2 == 1):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=self.robo2, font=self.fonteMapa)
                    self.b1.grid(row=xR2, column=yR2, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa00, bg=self.backgroudR2, font=self.fonteMapa)

                elif (xR2 == 0 and yR2 == 7):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=self.robo2)
                    self.b1.grid(row=xR2, column=yR2, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa66, bg=self.backgroudR2, font=self.fonteMapa)

                else:
                    self.b1 = Button(self.container7, padx=20, pady=10, text=self.robo2, font=self.fonteMapa)
                    self.b1.grid(row=xR2, column=yR2, padx=5, pady=5)
                    self.b1.config(bg=self.backgroudR2)

                # Desenha as posições das caças
                c = 0
                for n in self.cacas:
                    cacaX = int(self.cacas[c]["x"])
                    cacaY = int(self.cacas[c]["y"])
                    if (cacaX == 6 and cacaY == 1):
                        self.b1 = Button(self.container7, padx=20, pady=10, text="C%d" %(c+1), font=self.fonteMapa)
                        self.b1.grid(row=cacaX, column=cacaY, padx=5, pady=5)
                        self.b1.config(highlightbackground=self.backgroudMapa00, bg='white', font=self.fonteMapa)

                    elif (cacaX == 0 and cacaY == 7):
                        self.b1 = Button(self.container7, padx=20, pady=10, text='C%d' %(c+1))
                        self.b1.grid(row=cacaX, column=cacaY, padx=5, pady=5)
                        self.b1.config(highlightbackground=self.backgroudMapa66, bg='white', font=self.fonteMapa)

                    else:
                        self.b1 = Button(self.container7, padx=20, pady=10, text='C%d' %(c+1), font=self.fonteMapa)
                        self.b1.grid(row=cacaX, column=cacaY, padx=5, pady=5)
                        self.b1.config(bg='white')
                    c = (c + 1)


    def desenhaInfo(self):
        # --------------------- DADOS INICIAIS DE CADA ROBÔ ---------------------
        self.pos1 = "(%d, %d)" % (self.posX1, self.posY1)
        self.pos2 = "(%d, %d)" % (self.posX2, self.posY2)
        self.prox1 = "(-, -)"
        self.prox2 = "(-, -)"

        # self.dadosR1.set(
        #     ' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas1, self.pos1, self.prox1))
        # self.dadosR2.set(
        #     ' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas2, self.pos2, self.prox2))

        # self.dadosR1.set(
        #     ' Posição atual: %s \n Próxima posição: %s' % (self.pos1, self.pos1))
        # self.dadosR2.set(
        #     ' Posição atual: %s \n Próxima posição: %s' % (self.pos2, self.pos2))
        self.dadosR1 = (' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.status.r1_cacasEncontradas.__len__(), self.pos1, self.pos1))
        self.dadosR2 = (' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.status.r2_cacasEncontradas.__len__(), self.pos2, self.pos2))

        # ---------------- DADOS INICIAIS GERAIS ----------------
        self.totalCacas = self.cacas.__len__()  # Vê o tamanho da lista de caças
        self.cacasEncontradas = 0
        self.cacasRestantes = (self.totalCacas - self.cacasEncontradas)

        # self.dadosGerais.set('Total de caças: %d\n Caças encontradas: %d\n Caças restantes: %d' % (self.totalCacas, self.cacasEncontradas, self.cacasRestantes))
        self.dadosGerais = 'Total de caças: %d\n Caças encontradas: %d\n Caças restantes: %d' % (
        self.totalCacas, self.cacasEncontradas, self.cacasRestantes)
        # self.textoPausa.set('Pausa')

        # ------------------------------------------ CONFIGURANDO CONTAINERS ------------------------------------------
        # self.espaco = Label(self.container2, text='Informações', font=self.fontePadrao, pady="25").pack()
        # self.textbox = Label(self.container2, text='Informações', font=self.fontePadrao, width=25).pack()
        self.textbox = Label(self.container2, text=self.robo1, font=self.fontePadrao, bg=self.backgroudR1,
                             width=20).pack(side=LEFT)
        self.container2.pack(fill=X)
        self.textbox = Label(self.container3, text=self.dadosR1, font=self.fonteMenor, bg=self.backgroudDefault,
                             width=27, height=4, anchor=W, justify=LEFT).pack(side=LEFT)
        # self.container3.pack(fill=BOTH) #BOTH -> expande tanto horizontalmente e verticalmente
        self.container3.pack(fill=X)
        # self.parada = Label(self.container4, font=self.fontePadrao, textvariable=self.textoParadaR1, foreground="red", width=20).pack(side=LEFT)
        self.espaco = Label(self.container2, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.espaco = Label(self.container3, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.espaco = Label(self.container4, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.textbox = Label(self.container2, text=self.robo2, font=self.fontePadrao, bg=self.backgroudR2,
                             width=20).pack(side=RIGHT)
        self.textbox = Label(self.container3, text=self.dadosR2, font=self.fonteMenor, bg=self.backgroudDefault,
                             width=27, height=4, anchor=W, justify=LEFT).pack(side=RIGHT)
        # self.parada = Label(self.container4, font=self.fontePadrao, text=self.textoParadaR2, foreground="red", width=20).pack(side=RIGHT)
        self.textbox = Label(self.container5, text=self.dadosGerais, font=self.fonteMenor, bg=self.backgroudDefault,
                             width=62).pack()
        self.container5.pack(fill=X)

        # Se o robô pedir para validar alguma caça, o botão aparece, senão ele continua invisivel
        self.b2 = Button(self.container6, text='Validar caça', font=self.fontePadrao, command=self.validarCaca,
                         bg=self.backgroudDefault, width=20).pack()
        self.b3 = Button(self.container6, text='Pausa', font=self.fontePadrao, command=self.teste,
                         bg=self.backgroudDefault, width=20).pack()
        self.b4 = Button(self.container6, text='Fim de jogo', font=self.fontePadrao, command=self.apagaTexto,
                         bg=self.backgroudDefault, width=20).pack()

    def teste(self):
        self.validarCaca("G2", 1, 2)

    def validarCaca(self, nomeRobo, x, y):

        msg = "Validar caça (%d, %d) do robô %s?" % (x, y, nomeRobo)
        self.preso = True
        self.popup = Tk()
        self.popup.wm_title("Solicitação para validação de caça")
        label = Label(self.popup, text=msg, font=self.fonteMenor)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(self.popup, text="Sim", font=self.fonteMenor, command=self.botaoSim).pack(side=LEFT)
        B2 = Button(self.popup, text="Não", font=self.fonteMenor, command=self.botaoNao).pack(side=RIGHT)
        print("Antes de ser preso!")
        self.popup.mainloop()
        while(True):
            if(self.preso == True):
                print("")
            elif (self.preso == False):
                break
        return self.resposta
    # def getListaCacas(self):
    #
    #     # listaCacas = []
    #     #
    #     # c1 = Coordenada(1, 2)
    #     # c1 = self.transformaCoord(c1)
    #     # c2 = Coordenada(1, 3)
    #     # c2 = self.transformaCoord(c2)
    #     # c3 = Coordenada(1, 4)
    #     # c3 = self.transformaCoord(c3)
    #     # c4 = Coordenada(1, 5)
    #     # c4 = self.transformaCoord(c4)
    #     #
    #     # listaCacas.append(c1)
    #     # listaCacas.append(c2)
    #     # listaCacas.append(c3)
    #     # listaCacas.append(c4)
    #
    #     return listaCacas

    def botaoSim(self):
        self.preso = False
        self.resposta = True

    def botaoNao(self):
        self.preso = False
        self.resposta = False

    def transformaCoord(self, obj):
        c = Coordenada(abs(obj.getY()-6), abs(obj.getX() + 1))
        return c

    # def botaoDeTestes(self):
    #     # self.textoParadaR1.set("Parada de emergência")
    #     # print("Obstáculo")
    #     if (self.textoParadaR1.get() == "Partida pausada"): # se a partida já está pausada
    #         self.textoParadaR1.set('')
    #         self.textoPausa.set('Pausa')
    #     else:
    #         self.textoParadaR1.set("Partida pausada")
    #         print("Pausa")
    #         self.textoPausa.set('Continua')
    #
    #     # ------- DADOS VINDO DO SS -------
    #     # nR1 = "G1"
    #     # nR2 = "G2"
    #
    #     R1 = Coordenada(randint(0,6), randint(0,6))
    #     self.posR1X = R1.getX()
    #     self.posR1Y = R1.getY()
    #     R1 = self.transformaCoord(R1)
    #
    #     R2 = Coordenada(randint(0, 6), randint(0, 6))
    #     posR2X = R2.getX()
    #     posR2Y = R2.getY()
    #     R2 = self.transformaCoord(R2)
    #
    #     xProxR1 = randint(0, 6)
    #     yProxR1 = randint(0, 6)
    #
    #     xProxR2 = randint(0, 6)
    #     yProxR2 = randint(0, 6)
    #
    #     self.desenhaMapa(self.nomeR1, R1, self.nomeR2, R2)
    #
    #     # self.cacas1 = 2
    #     # self.cacas2 = 1
    #
    #     self.pos1 = "(%d, %d)" % (posR1X, posR1Y)
    #     self.pos2 = "(%d, %d)" % (posR2X, posR2Y)
    #
    #     self.prox1 = "(%d, %d)" % (xProxR1, yProxR1)
    #     self.prox2 = "(%d, %d)" % (xProxR2, yProxR2)
    #
    #     self.dadosR1.set(' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas1, self.pos1, self.prox1))
    #     self.dadosR2.set(' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas2, self.pos2, self.prox2))
    #     # MOSTRAR QUANDO O ROBÔ QUER VALIDAR CAÇA
    #
    #     # self.nomeR1.set(nR1)
    #     # self.nomeR2.set(nR2)
    #
    #     self.totalCacas = 7 # Total de caças que existem no mapa inteiro
    #     self.cacasEncontradas = (self.cacas1 + self.cacas2)
    #     self.cacasRestantes = (self.totalCacas - self.cacasEncontradas)
    #     self.dadosGerais.set('Total de caças: %d\n Caças encontradas: %d\n Caças restantes: %d' % (self.totalCacas, self.cacasEncontradas, self.cacasRestantes))

    def apagaTexto(self):
        self.textoParadaR1.set("")
        self.textoParadaR2.set("")

    def atualizaPartida(self):
        while True:

            compartilhados.transmitir_toUI_event.wait()

            with compartilhados.transmitir_toUI_lock:
                msg = deepcopy(compartilhados.transmitir_toUI)
                print("msg::: %s" % str(msg))

                if msg['cmd'] == MsgAuditorToUI.AtualizarRobo:
                    # Ja esta sendo atualizado no robo, precisa atualizar aqui tambem?

                    x, y = self.status.getCoordRobo(msg['_robo'])
                    print("Robo", msg['_robo'], "Posicao atual (" + str(x) +","+ str(y)+")")


                    msg = {'_dir': 'ui', 'cmd': MsgUItoAuditor.AtualizaMapa, '_robo': msg['_robo']}
                    self.avisar_gerenciador(msg)

                if msg['cmd'] == MsgAuditorToUI.ValidarCaca:
                    print("ROBO: " + msg['robo'] + " solicita validação de caça")
                    print("Na posição: ", '(', msg['x'], ',', msg['y'], ')')
                    x = 0
                    y = 0

                    if msg['robo'] == self.status.getRoboA():
                        x, y = self.status.getCoordRobo(self.status.getRoboA())
                        self.posX1 = x
                        self.posY1 = y
                        self.R1 = Coordenada(self.posX1, self.posY1)
                        self.R1 = self.transformaCoord(self.R1)
                        self.desenhaMapa()
                        self.desenhaInfo()

                    elif msg['robo'] == self.status.getRoboB():
                        x, y = self.status.getCoordRobo(self.status.getRoboB())
                        self.posX2 = x
                        self.posY2 = y
                        self.R2 = Coordenada(self.posX2, self.posY2)
                        self.R2 = self.transformaCoord(self.R2)
                        self.desenhaMapa()
                        self.desenhaInfo()

                    # print("POSICAO DO ROBO: ", "(", x, ",", y, ")")
                    while True:
                        v = self.validarCaca()
                        if v == 's':
                            self.status.atualizarCacas(msg['robo'], msg['x'], msg['y'])
                            msg = {'_robo': msg['robo'], '_dir': 'ui', 'cmd': MsgUItoAuditor.ValidarCaca,
                                   'validacao': 1, 'x': msg['x'], 'y': msg['y']}
                            self.avisar_gerenciador(msg)
                            break

                        else:
                            print("Comando invalido")
            compartilhados.transmitir_toUI_event.clear()


    def avisar_gerenciador(self, msg):
        with compartilhados.gerente_msg_lock:
            compartilhados.gerente_msg = msg
            compartilhados.solicita_gerente.set()
