from mover_test import *
# from mover import *
from interface import *
from threading import Thread, Lock
from shared import *
from time import sleep
from copy import deepcopy


class Automatico(Thread):
	"""Busca cacas de maneira autonoma"""
	def __init__(self, coord, cacas):
		global shared_obj
		shared_obj.set(SharedObj.AutomaticoPosicao, coord)
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
		shared_obj.set(SharedObj.InterfaceCacasAtualizadas, cacas)

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


	def _verifica_pausa(self):
		global shared_obj
		if shared_obj.get(SharedObj.InterfacePauseContinua):
			# Pausa setada, paramos e aguardamos algum evento ...
			shared_obj.set(SharedObj.MoverMovimento, Mover.PAUSA)
			
			while True:
				sleep(0.5)
				# Aguardamos duas coisas: continue ou fim do jogo
				if not shared_obj.get(SharedObj.InterfacePauseContinua):
					# Fim da pausa
					shared_obj.set(SharedObj.MoverMovimento, Mover.CONTINUA)
					return Mover.CONTINUA

				if shared_obj.get(SharedObj.InterfaceFimJogo):
					# Fim do jogo
					shared_obj.set(SharedObj.MoverMovimento, Mover.EXIT)
					return Mover.EXIT


	def _valida_caca(self, posicao):
		global shared_obj
		shared_obj.set(SharedObj.AutomaticoValidarCaca, 1)
		ret = True
		while True:
			if shared_obj.get(SharedObj.AutomaticoValidarCaca):
				sleep(1)
				continue

			posicao_validada = shared_obj.get(SharedObj.AutomaticoPosicao)
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
		global shared_obj
		self.cacas_ordenadas = shared_obj.get(SharedObj.InterfaceCacasAtualizadas)
		self._ordena_cacas()


	def _finaliza_tudo(self):
		global shared_obj
		shared_obj.set(SharedObj.MoverMovimento, Mover.EXIT)
		shared_obj.set(SharedObj.InterfaceFimJogo, 1)


	def _go(self):
		global shared_obj
		if not len(self.cacas_ordenadas):
			print("CACAS VAZIAS")
			self._finaliza_tudo()
			return

		caca = self.cacas_ordenadas.pop(0)
		print("PROXIMA CACA: %s" % str(caca))
		direcoes = self._calcula_direcoes(caca)
		print("DIRECOES : %s" % str(direcoes))
		while len(direcoes):
			print("Verifica pausa GO")
			if self._verifica_pausa() == Mover.EXIT:
				return
			direcao = direcoes.pop(0)
			self.informa_movimento(direcao)
			if shared_obj.get(SharedObj.MoverMovimento) == Mover.PARADO:
				shared_obj.set(SharedObj.MoverMovimento, direcao)

			while shared_obj.get(SharedObj.MoverMovimento) != Mover.PARADO:
				sleep(1)

			self.historico_mov.append(direcao)

		return caca


	def run(self):
		global shared_obj
		# Primeira vez só ordena as cacas e sai cavando
		self._ordena_cacas()
		while True:
			print("Verifica pausa RUN")
			if self._verifica_pausa() == Mover.EXIT:
				break

			posicao = self._go()
			if shared_obj.get(SharedObj.InterfaceFimJogo):
				break

			shared_obj.set(SharedObj.AutomaticoPosicao, posicao)
			validacao = self._valida_caca(posicao)
			if validacao:
				print("\nCACA VALIDADA!!\n")
				

			if not len(self.cacas_ordenadas):
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

