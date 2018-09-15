from manual import *
from automatico import *
# from mover import Mover, mutexHistorico, historico, verifica_mutex_historico
from mover_test import *


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
		if self.modo == ModoDeJogo.AUTOMATICO:
			seta_mutex_fim_jogo(1)
		else:
			seta_mutex_manual(Mover.EXIT)


	def novo_jogo(self, modo, coord_inicial, cacas=None):
		if modo == ModoDeJogo.MANUAL:
			seta_mutex_manual(Mover.PARADO)
			self.cacador = Manual(coord_inicial)

		elif modo == ModoDeJogo.AUTOMATICO:
			self.cacador = Automatico(coord_inicial, cacas)

		self.cacador.start()


	def mover_manual(self, direcao):
		if self.modo == ModoDeJogo.AUTOMATICO:
			print("Modo de jogo automatico, sem movimentos manuais!!")
			return

		seta_mutex_manual(direcao)


	def atualiza_cacas(self, cacas):
		seta_mutex_cacas_atualizadas(cacas)


	def get_status(self):
		return verifica_mutex_manual()


	def get_historico(self):
		return verifica_mutex_historico()


if __name__ == "__main__":
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
					if verifica_mutex_movimento() == 0:
						seta_mutex_movimento(Mover.FRENTE)
					else:
						print("Robo em movimento. Aguarde ...")
				elif str(cmd).lower() == 's':
					interface.mover_manual(Mover.TRAS)
					if verifica_mutex_movimento() ==  0:
						seta_mutex_movimento(Mover.TRAS)
					else:
						print("Robo em movimento. Aguarde ...")
				elif str(cmd).lower() == 'd':
					interface.mover_manual(Mover.DIREITA)
					if verifica_mutex_movimento() ==  0:
						seta_mutex_movimento(Mover.DIREITA)
					else:
						print("Robo em movimento. Aguarde ...")
				elif str(cmd).lower() == 'a':
					interface.mover_manual(Mover.ESQUERDA)
					if verifica_mutex_movimento() ==  0:
						seta_mutex_movimento(Mover.ESQUERDA)
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
			if verifica_mutex_fim_jogo():
				break

			caca_a_validar = verifica_mutex_caca_a_validar()
			if caca_a_validar:
				ok = input("Digite 1 para validar a caca ou 0 para invalidar: ")
				if not int(ok):
					pos_x = input("Digite a coordenada x: ")
					pos_y = input("Digite a coordenada y: ")
					pos = (int(pos_x), int(pos_y))
					seta_mutex_posicao_autonomo(pos)
				else:
					cacas_atuais = verifica_mutex_cacas_atualizadas()
					posicao = verifica_mutex_posicao_autonomo()
					cacas_atuais.remove(posicao)
					seta_mutex_cacas_atualizadas(cacas_atuais)

				seta_mutex_caca_a_validar(0)

			sleep(1)










