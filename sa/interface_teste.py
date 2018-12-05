import compartilhados
from copy import deepcopy
from mensagens_auditor import *
import random
from threading import Thread

class Inter(Thread):

    def __init__(self, status):
        Thread.__init__(self)
        self.status = status


    def avisar_gerenciador(self, msg):
        with compartilhados.gerente_msg_lock:
            compartilhados.gerente_msg = msg
            compartilhados.solicita_gerente.set()

    def run(self):

        print("========CONFIGURAÇÕES INICIAIS ===========")

        try:
            roboA = input("Nome do robo 1: ")
            x1 = int(input("Defina x inicial: "))
            y1 = int(input("Defina y inicial: "))
            roboB = input("Nome do robo 2: ")
            x2 = int(input("Defina x inicial: "))
            y2 = int(input("Defina y inicial: "))
        except Exception as e:
            print("Valor inicial invalido")
            exit()

        cacas = []

        # Sorteia cacas
        for i in range(0, 5):
            caca = {}
            caca["x"] = random.randint(1, 5)
            caca["y"] = random.randint(1, 5)
            cacas.append(caca)

        print("Cacas: %s" % str(cacas))

        # Define jogadores e caças
        self.status.definirPartida(roboA, x1, y1, roboB, x2, y2, cacas)

        # Seleciona o modo de Jogo
        modo = int(input("Definir modo de jogo\n (1) Manual \n (2) Automatico\n"))
        msg = {}
        if modo == 1:
            msg = {'_robo': '', "cmd": MsgUItoAuditor.NovoJogo, "modo_jogo": 1, "cacas": cacas,
                   'jogadorA': roboA, 'xA': x1, 'yA': y1, 'jogadorB': roboB, 'xB': x2, 'yB': y2, '_dir':'ui'}

        elif modo == 2:
            msg = {'_robo': '', "cmd": MsgUItoAuditor.NovoJogo, "modo_jogo": 2, "cacas": cacas,
                   'jogadorA': roboA, 'xA': x1, 'yA': y1, 'jogadorB': roboB, 'xB': x2, 'yB': y2, '_dir':'ui'}

        print(msg)
        # Envia para todos o modo de jogo
        self.avisar_gerenciador(msg)



        ## Interface de testes

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

                    elif msg['robo'] == self.status.getRoboB():
                        x, y = self.status.getCoordRobo(self.status.getRoboB())
                    print("POSICAO DO ROBO: ", "(", x, ",", y, ")")


                    while True:
                        v = input("VALIDAR?\n(s) SIM\n(n) NÃO\n")
                        if v == 's':
                            self.status.atualizarCacas(msg['robo'], msg['x'], msg['y'])
                            msg = {'_robo': msg['robo'], '_dir': 'ui', 'cmd': MsgUItoAuditor.ValidarCaca, 'validacao': 1, 'x': msg['x'], 'y': msg['y']}
                            self.avisar_gerenciador(msg)
                            break

                        else:
                            print("Comando invalido")





            compartilhados.transmitir_toUI_event.clear()