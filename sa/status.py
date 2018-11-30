from coordenada import *


class Status:

    # Inicia status de jogo sem nomes definidos para os robos
    # e coordenada inicial zero para ambos
    def __init__(self):
        # Atributos para Robo 1
        self.r1 = ''
        self.coord_r1 = Coordenada(0, 0)
        self.r1_cacasEncontradas = []

        # Atributos para o Robo 2
        self.r2 = ''
        self.coord_r2 = Coordenada(0, 0)
        self.r2_cacasEncontradas = []

        # Lista de cacas do jogo
        self.cacas = []

        self.vX = 0
        self.vY = 0

        # Recupera dados do DB
        self.dados_DB = []

    # Configuração do status da partida após definir quem será os jogadores
    # e suas coordenadas iniciais
    def definirPartida(self, nome_roboA, aX, aY, nome_roboB, bX, bY, listaCacas):
        self.r1 = nome_roboA
        self.coord_r1 = Coordenada(aX, aY)

        self.r2 = nome_roboB
        self.coord_r2 = Coordenada(bX, bY)

        self.cacas = listaCacas

    # Identifica se o Robo passado na mensagem é valido
    def _validarRobo(self, robo):
        return self.r1 == robo or self.r2 == robo

    def atualizarPosicaoRobo(self, robo, x, y):
        if not self._validarRobo(robo): return False
        if robo == self.r1:
            self.coord_r1.setX(x)
            self.coord_r1.setY(y)
        else:
            self.coord_r2.setX(x)
            self.coord_r2.setY(y)
        return True

    def atualizarCacaRobo(self, robo, caca):
        if not self._validarRobo(robo): return False
        if self.r1 == robo:
            self.r1_cacasEncontradas.append(caca)
        else:
            self.r2_cacasEncontradas.append(caca)

        for i in range(len(self.cacas)):
            if self.cacas[i]['x'] == caca['x'] and self.cacas[i]['y'] == caca['y']:
                del self.cacas[i]
                break

    def getCacas(self):
        return self.cacas

    # Retorna uma tupla contendo x e y
    def getCoordRobo(self, robo):
        if not self._validarRobo(robo): return False
        if robo == self.r1:
            return self.coord_r1.getX(), self.coord_r1.getY()
        else:
            return self.coord_r2.getY(), self.coord_r2.getY()

    def getRoboA(self):
        return self.r1

    def getRoboB(self):
        return self.r2

    def getCacaRobo(self, robo):
        if not self._validarRobo(robo): return False
        if robo == self.r1:
            return self.r1_cacasEncontradas
        else:
            return self.r2_cacasEncontradas

    # Atualizar caças é chamado no momento em que um robo solicita validar sua caça
    # Este metodo verifica a caça e se ela for valida, ele deleta ela da lista
    # Chamar este metodo implica em chamar getCacas() logo em seguida para verificar se a lista não está vazia
    def atualizarCacas(self, robo, x, y):
        if self._validarRobo(robo): return False
        for i in range(len(self.cacas)):
            caca = self.cacas[i]
            if caca['x'] == x and caca['y'] == y:
                self.atualizarCacaRobo(robo, caca[i])
                del self.cacas[i]
                return True
        return False

    def definirVencedor(self):
        if self.r1_cacasEncontradas > self.r1_cacasEncontradas:
            return self.r1
        else:
            return self.r2

    # Coordenada onde o robo diz ter encontrado a caça
    def validarCacas(self, x, y):
        self.vX = x
        self.vY = y

    def getValidarCacas(self):
        return self.vX, self.vY


    def setDBtoStatus(self, dadosDB):
        self.dados_DB = dadosDB

    def getDBfromStatus(self):
        return self.dados_DB