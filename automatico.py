# from mover_test import *
from mover import *
from interface import *
from threading import Thread, Lock
from time import sleep
from copy import deepcopy

mutexValidarCaca = Lock()
cacaAValidar = 0

mutexPosicaoAutonomo = Lock()
posicaoAutonomo = (0, 0)

mutexFimJogo = Lock()
mutexCacasAtualizadas = Lock()
fimDoJogo = 0
cacasAtualizadas = []

def verifica_mutex_fim_jogo():
	global fimDoJogo
	mutexFimJogo.acquire()
	ret = fimDoJogo
	mutexFimJogo.release()
	return ret

def seta_mutex_fim_jogo(val):
	global fimDoJogo
	mutexFimJogo.acquire()
	fimDoJogo = deepcopy(val)
	mutexFimJogo.release()

def verifica_mutex_cacas_atualizadas():
	global cacasAtualizadas
	mutexCacasAtualizadas.acquire()
	ret = deepcopy(cacasAtualizadas)
	mutexCacasAtualizadas.release()
	return ret


def seta_mutex_cacas_atualizadas(cacas):
	global cacasAtualizadas
	mutexCacasAtualizadas.acquire()
	cacasAtualizadas = deepcopy(cacas)
	mutexCacasAtualizadas.release()

def verifica_mutex_caca_a_validar():
	global cacaAValidar
	mutexValidarCaca.acquire()
	ret = deepcopy(cacaAValidar)
	mutexValidarCaca.release()
	return ret


def seta_mutex_caca_a_validar(val):
	global cacaAValidar
	mutexValidarCaca.acquire()
	cacaAValidar = deepcopy(val)
	mutexValidarCaca.release()


def verifica_mutex_posicao_autonomo():
	global posicaoAutonomo
	mutexPosicaoAutonomo.acquire()
	ret = deepcopy(posicaoAutonomo)
	mutexPosicaoAutonomo.release()
	return ret


def seta_mutex_posicao_autonomo(pos):
	global posicaoAutonomo
	mutexPosicaoAutonomo.acquire()
	posicaoAutonomo = deepcopy(pos)
	mutexPosicaoAutonomo.release()


class Automatico(Thread):
	"""Busca cacas de maneira autonoma"""
	def __init__(self, coord, cacas):
		global posicaoAutonomo
		posicaoAutonomo = deepcopy(coord)
		self.posicao_inicial = coord
		self.cacas = cacas
		self.cacas_ordenadas = cacas
		self.cacas_encontradas = [] 
		self.historico_mov = []
		self._x = coord[0]
		self._y = coord[1]
		self._ultima_dir = Mover.FRENTE

		self.movedor = Mover(self._x, self._y)
		self.movedor.start()
		seta_mutex_cacas_atualizadas(cacas)

		super(Automatico, self).__init__()


	def _ordena_cacas(self):
		if self.posicao_inicial == (6, 6):
			self.cacas_ordenadas.sort(reverse=True)
		else:
			self.cacas_ordenadas.sort()


	def _calcula_direcoes(self, proxima_coord):
		direcoes = []
		if self.posicao_inicial == (0,0):
			offset_x = proxima_coord[0] - self._x
			offset_y = proxima_coord[1] - self._y
		else:
			offset_x = self._x - proxima_coord[0]
			offset_y = self._y - proxima_coord[1]

		# Calcula novas direcoes, tentando fazer menos curva
		if self._ultima_dir == Mover.TRAS:
			if offset_y < 0:
				for i in range(offset_y, 0):
					direcoes.append(Mover.TRAS)
			if offset_x > 0:
				for i in range(0, offset_x):
					direcoes.append(Mover.DIREITA)
			if offset_x < 0:
				for i in range(offset_x, 0):
					direcoes.append(Mover.ESQUERDA)
			if offset_y > 0:
				for i in range(0, offset_y):
					direcoes.append(Mover.FRENTE)

		elif self._ultima_dir == Mover.DIREITA:
			if offset_x > 0:
				for i in range(0, offset_y):
					direcoes.append(Mover.DIREITA)
			if offset_y > 0:
				for i in range(0, offset_y):
					direcoes.append(Mover.FRENTE)
			if offset_y < 0:
				for i in range(offset_y, 0):
					direcoes.append(Mover.TRAS)
			if offset_x < 0:
				for i in range(offset_x, 0):
					direcoes.append(Mover.ESQUERDA)

		elif self._ultima_dir == Mover.ESQUERDA:
			if offset_x < 0:
				for i in range(offset_y, 0):
					direcoes.append(Mover.ESQUERDA)
			if offset_y > 0:
				for i in range(0, offset_y):
					direcoes.append(Mover.FRENTE)
			if offset_y < 0:
				for i in range(offset_y, 0):
					direcoes.append(Mover.TRAS)
			if offset_x > 0:
				for i in range(0, offset_x):
					direcoes.append(Mover.DIREITA)

		else:
			if offset_y > 0:
				for i in range(0, offset_y):
					direcoes.append(Mover.FRENTE)
			if offset_x > 0:
				for i in range(0, offset_x):
					direcoes.append(Mover.DIREITA)
			if offset_x < 0:
				for i in range(offset_x, 0):
					direcoes.append(Mover.ESQUERDA)
			if offset_y < 0:
				for i in range(offset_y, 0):
					direcoes.append(Mover.TRAS)

		return direcoes


	def _valida_caca(self, posicao):
		seta_mutex_caca_a_validar(1)
		ret = True
		while True:
			if verifica_mutex_caca_a_validar():
				sleep(1)
				continue

			posicao_validada = verifica_mutex_posicao_autonomo()
			if posicao_validada != posicao:
				# Caca invalidada!! Ajusta posicao!!
				ret = False
				posicao = posicao_validada
			else:
				self.cacas_encontradas.append(posicao)

			break

		self._x = posicao[0]
		self._y = posicao[1]
		# TODO: self.movedor.atualiza_coord(posicao)
		return ret


	def informa_movimento(self, direcao):
		# TODO: Implementacao para avisar SS
		print("Indo para %d" % direcao)


	def atualiza_cacas(self):
		self.cacas_ordenadas = verifica_mutex_cacas_atualizadas()
		self._ordena_cacas()


	def _finaliza_tudo(self):
		seta_mutex_movimento(Mover.EXIT)
		seta_mutex_fim_jogo(1)


	def _go(self):
		if not len(self.cacas_ordenadas):
			print("CACAS VAZIAS")
			self._finaliza_tudo()
			return

		caca = self.cacas_ordenadas.pop(0)
		print("PROXIMA CACA: %s" % str(caca))
		direcoes = self._calcula_direcoes(caca)
		print("DIRECOES : %s" % str(direcoes))
		while len(direcoes):
			direcao = direcoes.pop(0)
			self.informa_movimento(direcao)
			if verifica_mutex_movimento() == Mover.PARADO:
				seta_mutex_movimento(direcao)

			while verifica_mutex_movimento() != Mover.PARADO:
				sleep(1)

			self.historico_mov.append(direcao)

		return caca


	def run(self):
		# Primeira vez só ordena as cacas e sai cavando
		self._ordena_cacas()
		while True:
			posicao = self._go()
			seta_mutex_posicao_autonomo(posicao)
			validacao = self._valida_caca(posicao)
			if validacao:
				print("\nCACA VALIDADA!!\n")
				

			if verifica_mutex_fim_jogo() or not len(self.cacas_ordenadas):
				# FIM DO JOGO
				break

			self.atualiza_cacas()

		self._finaliza_tudo()
		print("FINALIZANDO ....")
		print("HISTORICO: %s" % str(self.historico_mov))
		print("CACAS ENCONTRADAS: %s" % str(self.cacas_encontradas))



# if __name__ == "__main__":
# 	coord_inicial = (0, 0)
# 	cacas = [(3, 2), (1, 1), (4, 2)]
# 	cacasAtualizadas = deepcopy(cacas)
# 	autonomo = Automatico(coord_inicial, cacas)
# 	autonomo.run()

