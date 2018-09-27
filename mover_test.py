from time import time, sleep
from threading import Thread, Lock
from copy import deepcopy
from shared import *

class Cor(object):
	# 0=unknown, 1=black, 2=blue, 3=green, 4=yellow, 5=red, 6=white, 7=brown
	INDEFINIDO = 0
	PRETO = 1
	AZUL = 2
	VERDE = 3
	AMARELO = 4
	VERMELHO = 5
	BRANCO = 6
	MARROM = 7

	corToString = {
		INDEFINIDO: 'indefinido',
		PRETO: 'preto',
		AZUL: 'azul',
		VERDE: 'verde',
		AMARELO: 'amarelo',
		VERMELHO: 'vermelho',
		BRANCO: 'branco',
		MARROM: 'marrom'
	}


class Mover(Thread):
	"""docstring for Mover"""
	EXIT = -1
	PARADO = 0
	FRENTE = 1
	DIREITA = 2
	TRAS = 3
	ESQUERDA = 4

	def __init__(self, x, y):
		# Atributos ocultos
		self._ultima_direcao = Mover.FRENTE
		self._min_ref = 5
		self._max_ref = 80
		self._pause = False
		self._coord_ini = (x, y)
		self._coord_x = x
		self._coord_y = y
		self._next_coord = (x, y)

		super(Mover, self).__init__()


	def _calc_next_coord(self, direcao, coord=None):
		coord_x = self._coord_x
		coord_y = self._coord_y

		if coord is not None:
			coord_x = coord[0]
			coord_y = coord[1]

		if self._coord_ini == (0, 0):
			if direcao == Mover.FRENTE:
				coord_y += 1
			elif direcao == Mover.DIREITA:
				coord_x += 1
			elif direcao == Mover.TRAS:
				coord_y -= 1
			elif direcao == Mover.ESQUERDA:
				coord_x -= 1

		elif self._coord_ini == (6, 6):
			if direcao == Mover.FRENTE:
				coord_y -= 1
			elif direcao == Mover.DIREITA:
				coord_x -= 1
			elif direcao == Mover.TRAS:
				coord_y += 1
			elif direcao == Mover.ESQUERDA:
				coord_x += 1

		return (coord_x, coord_y)


	def _finalizar_movimento(self):
		global shared_obj
		shared_obj.acquire(SharedObj.MoverMovimento)
		if shared_obj.get_directly(SharedObj.MoverMovimento) != Mover.EXIT:
			shared_obj.set_directly(SharedObj.MoverMovimento, Mover.PARADO)
		shared_obj.release(SharedObj.MoverMovimento)


	def move(self, direcao, coord_atual=None):
		"""Move em uma direcao (frente, direita, esquerda, tras).
			Se for passada a mesma direcao, calibra e segue em fente"""

		if direcao == Mover.PARADO or direcao == Mover.EXIT:
			return

		calc_coord = self._calc_next_coord(direcao, coord_atual)
		self._next_coord = calc_coord
		print("\nindo para: %s" % str(calc_coord))

		sleep(2)
		print("moved!")
		self._coord_x = calc_coord[0]
		self._coord_y = calc_coord[1]
		print("estamos em (%d, %d)" % (self._coord_x, self._coord_y))
		self._finalizar_movimento()

		#Salvar os movimentos no historico
		global shared_obj
		if direcao != Mover.PARADO and direcao != Mover.EXIT:
			shared_obj.append_list(SharedObj.MoverHistorico, direcao)


	def run(self):
		global shared_obj
		while True:
			move = shared_obj.get(SharedObj.MoverMovimento)

			if move != Mover.PARADO:
				self.move(move)

			if move == Mover.EXIT:
				break

			sleep(0.1)

