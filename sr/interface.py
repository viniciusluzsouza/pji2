from manual import *
from automatico import *
# from mover import *
from mover_test import *
from shared import *
from receptor import Receptor
from transmissor import Transmissor


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

		self.receptor = Receptor(50012, self)
		self.receptor.run()
		#self.identidade = self._get_mac()


	def _get_mac(self):
		mac = ""
		with open('/sys/class/net/wlan0/address', 'r') as f:
			mac = f.readline().rstrip()
		f.close()
		return mac


	def get_identidade(self):
		return "RG"


	def get_cor(self):
		return self.cor


	def fim_jogo(self):
		global shared_obj
		if self.modo == ModoDeJogo.AUTOMATICO:
			shared_obj.set(SharedObj.InterfaceFimJogo, 1)
		else:
			shared_obj.set(SharedObj.InterfaceFimJogo, 1)
			shared_obj.set(SharedObj.ManualMovimento, Mover.EXIT)
			shared_obj.set(SharedObj.MoverMovimento, Mover.EXIT)


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

	def pause(self):
		global shared_obj
		print("setando pausa")
		shared_obj.set(SharedObj.InterfacePauseContinua, 1)

	def continua(self):
		global shared_obj

		# Se mandar continuar, sem estar em pausa, nao faz nada
		if not shared_obj.get(SharedObj.InterfacePauseContinua):
			return

		print("continuando")
		shared_obj.set(SharedObj.InterfacePauseContinua, 0)

	def stop(self):
		self.pause()
		self.fim_jogo()


if __name__ == "__main__":
	interface = InterfaceSR()
	transmissor = Transmissor("localhost", 50015)
	transmissor.run()



