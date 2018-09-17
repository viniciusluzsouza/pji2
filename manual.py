# from mover_test import *
from mover import *
from interface import *
from threading import Thread, Lock
from time import sleep

mutexManual = Lock()
direcaoManual = 0

def verifica_mutex_manual():
	global direcaoManual
	mutexManual.acquire()
	ret = deepcopy(direcaoManual)
	mutexManual.release()
	return ret


def seta_mutex_manual(val):
	global direcaoManual
	mutexManual.acquire()
	direcaoManual = deepcopy(val)
	mutexManual.release()


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
		seta_mutex_movimento(direcao)
		while True:
			# Mutex manual vem da interface
			mut_manual = verifica_mutex_manual()
			if mut_manual == Mover.PARADO:
				seta_mutex_movimento(Mover.PARADO)

			if mut_manual == Mover.EXIT:
				seta_mutex_movimento(Mover.EXIT)

			# Mutex movimento é do mover (aguarda finalizar o movimento)
			if verifica_mutex_movimento() == Mover.PARADO:
				break

			sleep(1)

		if verifica_mutex_manual() != Mover.EXIT:
			seta_mutex_manual(Mover.PARADO)


	def run(self):
		while True:
			mov = verifica_mutex_manual()
			if mov != Mover.PARADO:
				if mov == Mover.EXIT:
					seta_mutex_movimento(Mover.EXIT)
					break

				self.move(mov)

			sleep(1)


