from manual import *
from automatico import *
# from mover import *
# from mover import Mover, mutexHistorico, historico, verifica_mutex_historico
from mover_test import *
from shared import *


class ModoDeJogo(object):
	MANUAL = 1
	AUTOMATICO = 2


class InterfaceSR(object):
	"""World interface for SR"""

	def __init__(self):
		self.cor = 1					# Valor definido fixo
		self.modo = None
		self.cacas = None
		self.cacador = None

		#self.identidade = self._get_mac()


	def _get_mac(self):
		mac = ""
		with open('/sys/class/net/wlan0/address', 'r') as f:
			mac = f.readline().rstrip()
		f.close()
		return mac


	def get_identidade(self):
		return self.identidade


	def get_cor(self):
		return self.cor


	def fim_jogo(self):
		global shared_obj
		if self.modo == ModoDeJogo.AUTOMATICO:
			shared_obj.set(SharedObj.InterfaceFimJogo, 1)
		else:
			shared_obj.set(SharedObj.ManualMovimento, Mover.EXIT)


	def novo_jogo(self, modo, coord_inicial, cacas=None):
		global shared_obj
		if modo == ModoDeJogo.MANUAL:
			shared_obj.set(SharedObj.ManualMovimento, Mover.PARADO)
			self.cacador = Manual(coord_inicial)

		elif modo == ModoDeJogo.AUTOMATICO:
			self.cacador = Automatico(coord_inicial, cacas)

		self.cacador.start()


	def mover_manual(self, direcao):
		global shared_obj
		if self.modo == ModoDeJogo.AUTOMATICO:
			print("Modo de jogo automatico, sem movimentos manuais!!")
			return

		shared_obj.set(SharedObj.ManualMovimento, direcao)


	def atualiza_cacas(self, cacas):
		global shared_obj
		shared_obj.set(SharedObj.InterfaceCacasAtualizadas, cacas)


	def get_status(self):
		global shared_obj
		return shared_obj.get(SharedObj.MoverMovimento)


	def get_historico(self):
		global shared_obj
		return shared_obj.get(SharedObj.MoverHistorico)

if __name__ == "__main__":
	global shared_obj
	coord_ini = (0, 0)
	modo_jogo = ModoDeJogo.MANUAL
	cacas = [(2,4), (5,5), (1,1)]
	interface = InterfaceSR()
	interface.novo_jogo(modo=modo_jogo, coord_inicial=coord_ini, cacas=cacas)

	if modo_jogo == ModoDeJogo.MANUAL:
		while True:
			cmd = input("Digite o comando: ")
			try:
				if str(cmd).lower() == 'w':
					interface.mover_manual(Mover.FRENTE)
					if shared_obj.get(SharedObj.MoverMovimento) == 0:
						shared_obj.set(SharedObj.MoverMovimento, Mover.FRENTE)
					else:
						print("Robo em movimento. Aguarde ...")
				elif str(cmd).lower() == 's':
					interface.mover_manual(Mover.TRAS)
					if shared_obj.get(SharedObj.MoverMovimento) ==  0:
						shared_obj.set(SharedObj.MoverMovimento, Mover.TRAS)
					else:
						print("Robo em movimento. Aguarde ...")
				elif str(cmd).lower() == 'd':
					interface.mover_manual(Mover.DIREITA)
					if shared_obj.get(SharedObj.MoverMovimento) ==  0:
						shared_obj.set(SharedObj.MoverMovimento, Mover.DIREITA)
					else:
						print("Robo em movimento. Aguarde ...")
				elif str(cmd).lower() == 'a':
					interface.mover_manual(Mover.ESQUERDA)
					if shared_obj.get(SharedObj.MoverMovimento) ==  0:
						shared_obj.set(SharedObj.MoverMovimento, Mover.ESQUERDA)
					else:
						print("Robo em movimento. Aguarde ...")
				elif str(cmd).lower() == 'b':
					interface.fim_jogo()
					break
				elif str(cmd).lower() == 'q':
					interface.fim_jogo()
					break
				else:
					print("Comando nao identificado.")

			except Exception as e:
				raise Exception('ERRO: %s' % str(e))
				raise Exception(str(e))

	else:
		print("AUTONOMO MODE ON!!")
		while True:
			if shared_obj.get(SharedObj.InterfaceFimJogo):
				break

			caca_a_validar = shared_obj.get(SharedObj.AutomaticoValidarCaca)
			if caca_a_validar:
				ok = input("Digite 1 para validar a caca ou 0 para invalidar: ")
				if not int(ok):
					pos_x = input("Digite a coordenada x: ")
					pos_y = input("Digite a coordenada y: ")
					pos = (int(pos_x), int(pos_y))
					shared_obj.set(SharedObj.AutomaticoPosicao, pos)
				else:
					cacas_atuais = shared_obj.get(SharedObj.InterfaceCacasAtualizadas)
					posicao = shared_obj.get(SharedObj.AutomaticoPosicao)
					cacas_atuais.remove(posicao)
					shared_obj.set(SharedObj.InterfaceCacasAtualizadas, cacas_atuais)

				shared_obj.set(SharedObj.AutomaticoValidarCaca, 0)

			sleep(0.1)










