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
		msg = {'cmd': MsgSRtoSS.ValidaCaca, 'x': posicao[0], 'y': posicao[1]}
		resp = self._envia_msg(msg)

		if 'ack' in resp and resp['ack']:
			self._x = posicao[0]
			self._y = posicao[1]
			self.cacas_encontradas.append()
			self.cacas_ordenadas.remove(posicao)
			return 1

		if 'buffer' in resp:
			buf = resp['buffer']
			if 'x' in buf: self._x = buf['x']
			if 'y' in buf: self._y = buf['y']
			return 0

		else:
			return 0

	def _calc_next_coord(self, direcao, coord=None):
		coord_x = self._x
		coord_y = self._y

		if coord is not None:
			coord_x = coord[0]
			coord_y = coord[1]

		if self.coord_inicial == (0, 0):
			if direcao == Mover.FRENTE:
				coord_y += 1
			elif direcao == Mover.DIREITA:
				coord_x += 1
			elif direcao == Mover.TRAS:
				coord_y -= 1
			elif direcao == Mover.ESQUERDA:
				coord_x -= 1

		elif self.coord_inicial == (6, 6):
			if direcao == Mover.FRENTE:
				coord_y -= 1
			elif direcao == Mover.DIREITA:
				coord_x -= 1
			elif direcao == Mover.TRAS:
				coord_y += 1
			elif direcao == Mover.ESQUERDA:
				coord_x += 1

		return (coord_x, coord_y)

	def _envia_msg(self, msg):
		shared_obj.acquire(SharedObj.TransmitirLock)
		shared_obj.set_directly(SharedObj.TransmitirMsg, msg)
		shared_obj.set_event(SharedObj.TransmitirMsg)

		shared_obj.wait_event(SharedObj.TransmitirResp)
		resp = shared_obj.get_directly(SharedObj.TransmitirResp)
		shared_obj.clear_event(SharedObj.TransmitirResp)
		shared_obj.release(SharedObj.TransmitirLock)
		return resp


	def informa_movimento_ss(self, direcao):
		global shared_obj
		proxima_coord = self._calc_next_coord(direcao)
		msg = {'cmd': MsgSRtoSS.MovendoPara, 'x': proxima_coord[0], 'y': proxima_coord[1]}
		self._envia_msg(msg)

	def informa_posicao(self):
		global shared_obj
		msg = {'cmd': MsgSRtoSS.PosicaoAtual, 'x': self._x, 'y': self._y}
		self._envia_msg(msg)

	def atualiza_cacas(self):
		# TODO: Implementar via rede
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
			self.informa_movimento_ss(direcao)
			if shared_obj.get(SharedObj.MoverMovimento) == Mover.PARADO:
				shared_obj.set(SharedObj.MoverMovimento, direcao)

			while shared_obj.get(SharedObj.MoverMovimento) != Mover.PARADO:
				sleep(1)

			self.historico_mov.append(direcao)

		return caca


	def run(self):
		global shared_obj
		# Primeira vez so ordena as cacas e sai cavando
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

			# self.atualiza_cacas()

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

