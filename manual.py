from mover_test import *
# from mover import *
from interface import *
from threading import Thread, Lock
from time import sleep
from shared import *


class Manual(Thread):
	def __init__(self, coord):
		self.posicao_inicial = coord
		self.historico_mov = []
		self._x = coord[0]
		self._y = coord[1]
		self._ultima_dir = Mover.FRENTE

		self.movedor = Mover(self._x, self._y)
		self.movedor.start()

		super(Manual, self).__init__()


	def move(self, direcao):
		global shared_obj
		shared_obj.set(SharedObj.ManualMovimento, direcao)
		while True:
			# Mutex manual vem da interface
			mut_manual = shared_obj.get(SharedObj.ManualMovimento)
			if mut_manual == Mover.PARADO:
				shared_obj.set(SharedObj.MoverMovimento, Mover.PARADO)

			if mut_manual == Mover.EXIT:
				shared_obj.set(SharedObj.MoverMovimento, Mover.EXIT)

			# Mutex movimento é do mover (aguarda finalizar o movimento)
			if shared_obj.get(SharedObj.MoverMovimento) == Mover.PARADO:
				break

			sleep(0.1)

		if shared_obj.get(SharedObj.ManualMovimento) != Mover.EXIT:
			shared_obj.set(SharedObj.ManualMovimento, Mover.PARADO)


	def run(self):
		global shared_obj
		while True:
			mov = shared_obj.get(SharedObj.ManualMovimento)
			if mov != Mover.PARADO:
				if mov == Mover.EXIT:
					shared_obj.set(SharedObj.MoverMovimento, Mover.EXIT)
					break

				self.move(mov)

			sleep(0.1)


