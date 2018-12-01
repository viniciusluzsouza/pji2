#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from random import randint

from coordenada import *
from gerente_db import *

class InterfaceGrafica:

    def __init__(self):
        dados = Tk()
        mapa = Tk()
        dados.title("Informações")
        mapa.title("Mapa")
        self.fontePadrao = ("Arial", "40")
        self.fonteMenor = ("Arial", "30")
        self.fonteMapa = ('Helvetica 12 bold')
        self.backgroudDefault = "gray75"

        # ------------- DADOS -------------
        self.nomeR1 = ""
        self.nomeR2 = ""
        self.cacas1 = 0
        self.cacas2 = 0
        self.textoParadaR1 = StringVar() # texto "Parada de emergência"
        self.textoParadaR2 = StringVar()
        self.dadosR1 = StringVar() # qtd cacas encontradas, pos atual e prox pos
        self.dadosR2 = StringVar()
        self.dadosGerais = StringVar() # total cacas, cacas encontradas e cacas restantes
        self.textoPausa = StringVar() # escreve pausa ou continua, dependendo da status do robô

        # ----- OBTENDO INFORMAÇÕES DO BANCO DE DADOS -----
        self.gerente_db = GerenteDB()
        self.partidas = self.gerente_db.get_partidas()
        self.cadastros = self.gerente_db.get_partidas()

        for partida in self.partidas:
            # print(cadastro.get('nome'))
            self.nomeR1 = partida.get('robo_a')
            self.nomeR2 = partida.get('robo_b')

        # i = 0
        # for cadastro in self.cadastros:
        #     self.backgroud[i] = cadastro.get('cor')
        #     i = i + 1

        '''
        FALTA NO BANCO DE DADOS:
            - Posições atuais de cada robô
            - Próximas posições de cada robô
            - Quantidade de caças existentes no tabuleiro todo
            - Seria melhor se fosse cor1 e cor2, pois aí fica em duas variáveis, ou criar um vetor self.backgroud[i]
        '''

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
        self.container8 = Frame(mapa)
        self.container9 = Frame(mapa)
        self.container10 = Frame(dados)
        self.container11 = Frame(dados)

        # adicionando os containers
        self.container1.pack()
        self.container2.pack()
        self.container3.pack()
        self.container4.pack()
        self.container5.pack()
        self.container6.pack()
        self.container7.pack()
        self.container8.pack()
        self.container9.pack()
        self.container10.pack()
        self.container11.pack()

        # ---------- MAPA ----------
        mapa.geometry("1000x700")
        # mapa.configure(background="Gray")

        self.espaco = Label(self.container1, text='Mapa', font=self.fontePadrao, pady="50").pack()

        # self.desenhaMapa("G1", 0, 7, "G2", 6,1)

        R1 = Coordenada(0, 0)
        R1 = self.transformaCoord(R1)

        R2 = Coordenada(6, 6)
        R2 = self.transformaCoord(R2)

        self.desenhaMapa(self.nomeR1, R1, self.nomeR2, R2, self.getListaCacas())

        # --------------------- DADOS INICIAIS DE CADA ROBÔ ---------------------
        self.pos1 = "(0, 0)"
        self.pos2 = "(6, 6)"
        self.prox1 = "(-, -)"
        self.prox2 = "(-, -)"

        self.dadosR1.set(' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas1, self.pos1, self.prox1))
        self.dadosR2.set(' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas2, self.pos2, self.prox2))

        # ---------------- DADOS INICIAIS GERAIS ----------------
        self.totalCacas = 0 # Vê o tamanho da lista de caças
        self.cacasEncontradas = 0
        self.cacasRestantes = (self.totalCacas - self.cacasEncontradas)

        self.dadosGerais.set('Total de caças: %d\n Caças encontradas: %d\n Caças restantes: %d' % (self.totalCacas, self.cacasEncontradas, self.cacasRestantes))

        self.textoPausa.set('Pausa')

        # ------------------------------------------ CONFIGURANDO CONTAINERS ------------------------------------------
        #self.espaco = Label(self.container2, text='Informações', font=self.fontePadrao, pady="25").pack()
        #self.textbox = Label(self.container2, text='Informações', font=self.fontePadrao, width=25).pack()
        self.textbox = Label(self.container2, text=self.nomeR1, font=self.fontePadrao, bg = self.backgroudR1, width = 20).pack(side=LEFT)
        self.container2.pack(fill=X)
        self.textbox = Label(self.container3, textvariable=self.dadosR1, font=self.fonteMenor, bg=self.backgroudDefault, width=27, height=4, anchor=W, justify=LEFT).pack(side=LEFT)
        #self.container3.pack(fill=BOTH) #BOTH -> expande tanto horizontalmente e verticalmente
        self.container3.pack(fill=X)
        self.parada = Label(self.container4, font=self.fontePadrao, textvariable=self.textoParadaR1, foreground= "red", width=20).pack(side=LEFT)
        self.espaco = Label(self.container2, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.espaco = Label(self.container3, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.espaco = Label(self.container4, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.textbox = Label(self.container2, text=self.nomeR2, font=self.fontePadrao, bg=self.backgroudR2, width = 20).pack(side=RIGHT)
        self.textbox = Label(self.container3, textvariable=self.dadosR2, font=self.fonteMenor, bg=self.backgroudDefault, width=27, height=4, anchor=W, justify=LEFT).pack(side=RIGHT)
        self.parada = Label(self.container4, font=self.fontePadrao, textvariable=self.textoParadaR2, foreground="red", width=20).pack(side=RIGHT)
        self.textbox = Label(self.container5, textvariable=self.dadosGerais, font=self.fonteMenor, bg=self.backgroudDefault, width=62).pack()
        self.container5.pack(fill=X) #VERIFICAR SE FUNCIONA

        # Se o robô pedir para validar alguma caça, o botão aparece, senão ele continua invisivel
        self.b2 = Button(self.container6, text='Validar caça', font=self.fontePadrao, command=self.validarCaca, bg=self.backgroudDefault, width=20).pack()
        self.b3 = Button(self.container6, textvariable=self.textoPausa, font=self.fontePadrao, command=self.botaoDeTestes, bg=self.backgroudDefault, width=20).pack()
        self.b4 = Button(self.container6, text='Fim de jogo', font=self.fontePadrao, command=self.apagaTexto, bg=self.backgroudDefault, width=20).pack()

        dados.mainloop()
        mapa.mainloop()

    def desenhaMapa(self, nomeR1, posR1, nomeR2, posR2, listaCacas):

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
                xR1 = posR1.getX()
                yR1 = posR1.getY()
                if (xR1 == 6 and yR1 == 1):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=nomeR1, font=self.fonteMapa)
                    self.b1.grid(row=xR1, column=yR1, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa00, bg=self.backgroudR1)

                elif (xR1 == 0 and yR1 == 7):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=nomeR1)
                    self.b1.grid(row=xR1, column=yR1, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa66, bg=self.backgroudR1,font=self.fonteMapa)

                else:
                    self.b1 = Button(self.container7, padx=20, pady=10, text=nomeR1, font=self.fonteMapa)
                    self.b1.grid(row=xR1, column=yR1, padx=5, pady=5)
                    self.b1.config(bg=self.backgroudR1)

                # Desenha posição do robô 2
                xR2 = posR2.getX()
                yR2 = posR2.getY()
                if (xR2 == 6 and yR2 == 1):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=nomeR2, font=self.fonteMapa)
                    self.b1.grid(row=xR2, column=yR2, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa00, bg=self.backgroudR2, font=self.fonteMapa)

                elif (xR2 == 0 and yR2 == 7):
                    self.b1 = Button(self.container7, padx=20, pady=10, text=nomeR2)
                    self.b1.grid(row=xR2, column=yR2, padx=5, pady=5)
                    self.b1.config(highlightbackground=self.backgroudMapa66, bg=self.backgroudR2, font=self.fonteMapa)

                else:
                    self.b1 = Button(self.container7, padx=20, pady=10, text=nomeR2, font=self.fonteMapa)
                    self.b1.grid(row=xR2, column=yR2, padx=5, pady=5)
                    self.b1.config(bg=self.backgroudR2)

                # Desenha as posições das caças
                c = 0
                for n in listaCacas:
                    cacaX = listaCacas[c].getX()
                    cacaY = listaCacas[c].getY()
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

    def validarCaca(self):
        # AQUI FICA A LÓGICA DO VALIDA CAÇA

        # SE FOI O R2 QUE PEDIU
        self.textoParadaR2.set("Caça (x, y) validada")

    def getListaCacas(self):

        listaCacas = []

        c1 = Coordenada(1, 2)
        c1 = self.transformaCoord(c1)
        c2 = Coordenada(1, 3)
        c2 = self.transformaCoord(c2)
        c3 = Coordenada(1, 4)
        c3 = self.transformaCoord(c3)
        c4 = Coordenada(1, 5)
        c4 = self.transformaCoord(c4)

        listaCacas.append(c1)
        listaCacas.append(c2)
        listaCacas.append(c3)
        listaCacas.append(c4)

        return listaCacas

    def transformaCoord(self, obj):
        c = Coordenada(abs(obj.getY()-6), abs(obj.getX() + 1))
        return c

    def botaoDeTestes(self):
        # self.textoParadaR1.set("Parada de emergência")
        # print("Obstáculo")
        if (self.textoParadaR1.get() == "Partida pausada"): # se a partida já está pausada
            self.textoParadaR1.set('')
            self.textoPausa.set('Pausa')
        else:
            self.textoParadaR1.set("Partida pausada")
            print("Pausa")
            self.textoPausa.set('Continua')

        # ------- DADOS VINDO DO SS -------
        # nR1 = "G1"
        # nR2 = "G2"

        R1 = Coordenada(randint(0,6), randint(0,6))
        posR1X = R1.getX()
        posR1Y = R1.getY()
        R1 = self.transformaCoord(R1)

        R2 = Coordenada(randint(0, 6), randint(0, 6))
        posR2X = R2.getX()
        posR2Y = R2.getY()
        R2 = self.transformaCoord(R2)

        xProxR1 = randint(0, 6)
        yProxR1 = randint(0, 6)

        xProxR2 = randint(0, 6)
        yProxR2 = randint(0, 6)

        self.desenhaMapa(self.nomeR1, R1, self.nomeR2, R2, self.getListaCacas())

        # self.cacas1 = 2
        # self.cacas2 = 1

        for partida in self.partidas:
            self.cacas1 = partida.get('cacas_a')
            self.cacas2 = partida.get('cacas_b')

        self.pos1 = "(%d, %d)" % (posR1X, posR1Y)
        self.pos2 = "(%d, %d)" % (posR2X, posR2Y)

        self.prox1 = "(%d, %d)" % (xProxR1, yProxR1)
        self.prox2 = "(%d, %d)" % (xProxR2, yProxR2)

        self.dadosR1.set(' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas1, self.pos1, self.prox1))
        self.dadosR2.set(' Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas2, self.pos2, self.prox2))
        # MOSTRAR QUANDO O ROBÔ QUER VALIDAR CAÇA

        # self.nomeR1.set(nR1)
        # self.nomeR2.set(nR2)

        self.totalCacas = 7 # Total de caças que existem no mapa inteiro
        self.cacasEncontradas = (self.cacas1 + self.cacas2)
        self.cacasRestantes = (self.totalCacas - self.cacasEncontradas)
        self.dadosGerais.set('Total de caças: %d\n Caças encontradas: %d\n Caças restantes: %d' % (self.totalCacas, self.cacasEncontradas, self.cacasRestantes))

    def apagaTexto(self):
        self.textoParadaR1.set("")
        self.textoParadaR2.set("")
