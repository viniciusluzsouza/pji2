from mover_test import *
# from mover import *
from interface import *
from threading import Thread, Lock
from shared import *
from time import sleep
from copy import deepcopy
from mensagens_robo import *
from receptor import *
from transmissor import *

class Automatico(Thread):
	"""Busca cacas de maneira autonoma"""
	def __init__(self, coord, cacas):
		global shared_obj
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


	def _valida_caca(self):
		global shared_obj
		posicao = shared_obj.get(SharedObj.MoverCoordenada)
		msg = {'cmd': MsgSRtoSS.ValidaCaca, 'x': posicao[0], 'y': posicao[1]}

		shared_obj.clear_event(SharedObj.InterfaceRespValidaCacaEvent)
		self._envia_msg(msg)
		shared_obj.wait_event(SharedObj.InterfaceRespValidaCacaEvent)
		resp = shared_obj.get(SharedObj.InterfaceRespValidaCacaMsg)

		if 'ack' in resp:
			if resp['ack']:
				# Caca validada!
				self._x = posicao[0]
				self._y = posicao[1]
				self.cacas_encontradas.append(posicao)
				return (True, False)	# Retorna caca validada e posicao nao reajustada

			elif 'x' in resp and 'y' in resp:
				self._x = resp['x']
				self._y = resp['y']
				shared_obj.set(SharedObj.MoverCoordenada, (self._x, self._y))
				return (False, True)	# Retorna caca nao validada e posicao reajustada

		return (False, False)	# Caso de erro: nao conseguiu validar e nem ajustar posicao

	def _envia_msg(self, msg):
		global shared_obj
		shared_obj.set(SharedObj.TransmitirLock, msg)
		shared_obj.set_event(SharedObj.TransmitirEvent)

	def _informa_movimento_ss(self, x, y):
		global shared_obj
		msg = {'cmd': MsgSRtoSS.MovendoPara, 'x': x, 'y': y}
		self._envia_msg(msg)

	def _informa_posicao(self):
		global shared_obj
		posicao = shared_obj.get(SharedObj.MoverCoordenada)
		self._x = posicao[0]
		self._y = posicao[1]
		msg = {'cmd': MsgSRtoSS.PosicaoAtual, 'x': posicao[0], 'y': posicao[1]}
		self._envia_msg(msg)

	def atualiza_cacas(self):
		global shared_obj
		# self.cacas_ordenadas = shared_obj.get(SharedObj.InterfaceCacasAtualizadas)
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
			self._informa_posicao()

			print("Verifica pausa GO")
			if self._verifica_pausa() == Mover.EXIT:
				return

			direcao = direcoes.pop(0)
			# Limpa evento mover coordenada e seta direcao
			shared_obj.clear_event(SharedObj.MoverCoordenadaEvent)
			if shared_obj.get(SharedObj.MoverMovimento) == Mover.PARADO:
				shared_obj.set(SharedObj.MoverMovimento, direcao)

			# Espera calcular a proxima coordenada
			shared_obj.wait_event(SharedObj.MoverCoordenadaEvent)
			# Envia ao SS a coordenada que o robo esta indo
			prox_coord = shared_obj.get(SharedObj.MoverCoordenada)
			self._informa_movimento_ss(prox_coord[0], prox_coord[1])

			while shared_obj.get(SharedObj.MoverMovimento) != Mover.PARADO:
				sleep(1)

			self.historico_mov.append(direcao)


	def run(self):
		global shared_obj
		# Primeira vez so ordena as cacas e sai cavando
		self._ordena_cacas()
		while True:
			print("Verifica pausa RUN")
			if self._verifica_pausa() == Mover.EXIT:
				break

			self._go()
			if shared_obj.get(SharedObj.InterfaceFimJogo):
				break

			ack, pos = self._valida_caca()
			if ack:
				print("\nCACA VALIDADA!!\n")
			elif pos:
				print("\nCACA INVALIDADA. POSICAO AJUSTADA\n")
			else:
				print("\nCACA INVALIDADE E POSICAO NAO AJUSTADA. E AGORA?\nVAMOS ABORTAR !")
				# TODO: situacao de erro, pensar o que fazer
				break

			if not len(self.cacas_ordenadas):
				# FIM DO JOGO
				break

			self.atualiza_cacas()

		self._finaliza_tudo()
		print("FINALIZANDO ....")
		print("HISTORICO: %s" % str(self.historico_mov))
		print("CACAS ENCONTRADAS: %s" % str(self.cacas_encontradas))