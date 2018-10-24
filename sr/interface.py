from manual import *
from automatico import *
# from mover import *
from mover_test import *
from shared import *
from receptor import Receptor
from transmissor import Transmissor
from time import sleep
from threading import Thread

class ModoDeJogo(object):
	MANUAL = 1
	AUTOMATICO = 2


class InterfaceSR(Thread):
	"""World interface for SR"""

	def __init__(self):
		self.cor = 1					# Valor definido fixo ?
		self.modo = None
		self.cacas = None
		self.cacador = None
		self.mac = "00:00:00:00:00:00"
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


	def novo_jogo(self, msg):
		global shared_obj

		ret = {'cmd': MsgSRtoSS.NovoJogoConfigurado, 'ack': 0}
		if 'modo_jogo' not in msg:
			ret['erro'] = MsgRoboErro.ParametroNaoInformado
			ret['param'] = 'modo_jogo'
			return ret
		else:
			self.modo_jogo = msg['modo_jogo']

		if 'coord_inicial' not in msg:
			ret['erro'] = MsgRoboErro.ParametroNaoInformado
			ret['param'] = 'coord_inicial'
			return ret
		else:
			self.coord_inicial = msg['coord_inicial']

		if msg['modo_jogo'] == ModoDeJogo.AUTOMATICO \
			and 'cacas' not in msg:
			ret['erro'] = MsgRoboErro.ParametroNaoInformado
			ret['param'] = 'cacas'
			return ret
		else:
			self.cacas = msg['cacas']

		if modo == ModoDeJogo.MANUAL:
			shared_obj.set(SharedObj.ManualMovimento, Mover.PARADO)
			self.cacador = Manual(coord_inicial)

		elif modo == ModoDeJogo.AUTOMATICO:
			self.cacador = Automatico(coord_inicial, cacas)

		self.cacador.start()
		ret['ack'] = 1
		return ret


	def mover_manual(self, direcao):
		global shared_obj
		if self.modo == ModoDeJogo.AUTOMATICO:
			print("Modo de jogo automatico, sem movimentos manuais!!")
			return

		shared_obj.set(SharedObj.ManualMovimento, direcao)


	def _atualiza_cacas(self, cacas):
		global shared_obj
		shared_obj.set(SharedObj.InterfaceCacasAtualizadas, cacas)


	def _atualiza_pos_adv(self, pos):
		# TODO
		pass


	def atualiza_mapa(self, msg):
		if 'cacas' in msg:
			self._atualiza_cacas(msg['cacas'])

		if 'posicao_adversario' in msg:
			self._atualiza_pos_adv(msg['posicao_adversario'])

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


	def _envia_msg(self, msg):
		shared_obj.set(SharedObj.TransmitirLock, msg)
		shared_obj.set_event(SharedObj.TransmitirEvent)


	def run(self):
		global shared_obj
		while True:
			# Espera alguma mensagem ...
			shared_obj.wait_event(SharedObj.InterfaceEvent)

			shared_obj.acquire(SharedObj.InterfaceEventMsg)
			msg = shared_obj.get_directly(SharedObj.InterfaceEventMsg)
			if 'cmd' not in msg:
				continue

			cmd = msg['cmd']

			# Mensagens vindas do SS:
			if cmd == MsgSStoSR.SolicitaID:
				resp = {'cmd': MsgSRtoSS.SolicitaID_Resp}
				resp['cor'] = self.cor
				resp['mac'] = self.mac
				self._envia_msg(resp)

			elif cmd == MsgSStoSR.NovoJogo:
				resp = self.novo_jogo(msg):
				self._envia_msg(resp)

			elif cmd == MsgSStoSR.Pausa:
				self.pause()

			elif cmd == MsgSStoSR.FimJogo:
				self.fim_jogo()

			elif cmd == MsgSStoSR.Mover:
				if self.modo_jogo is ModoDeJogo.MANUAL:
					self.mover_manual()

			elif cmd == MsgSStoSR.AtualizaMapa:
				if self.modo_jogo is ModoDeJogo.AUTOMATICO:
					self.atualiza_mapa()

			elif cmd == MsgSStoSR.ValidacaoCaca:
				shared_obj.set(InterfaceRespMsg, msg)
				shared_obj.set_event(InterfaceRespEvent)

			# Mensagens internas (do proprio SR)
			elif cmd == MsgSRtoSS.MovendoPara or \
				cmd == MsgSRtoSS.PosicaoAtual or \
				cmd == MsgSRtoSS.ValidaCaca or \
				cmd == MsgSRtoSS.ObstaculoEncontrado:
				self._envia_msg(msg)

			else:
				pass

			shared_obj.release(SharedObj.InterfaceEventMsg)
			shared_obj.clear_event(SharedObj.InterfaceEvent)


# if __name__ == "__main__":
# 	#interface = InterfaceSR()
# 	transmissor = Transmissor("localhost")
# 	transmissor.start()

# 	receptor = Receptor("localhost")
# 	receptor.start()

# 	for cmd in range (1000, 1004):
# 		print("ENTER PARA ENVIAR MENSAGEM AO SS")
# 		raw_input()

# 		msg = {'cmd': cmd}
# 		shared_obj.set(SharedObj.TransmitirLock, msg)
# 		shared_obj.set_event(SharedObj.TransmitirEvent)

# 		sleep(2)





