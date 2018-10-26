from manual import *
from automatico import *
# from mover import *
from mover_test import *
from shared import *
from receptor import *
from transmissor import *
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
		self.cacas = []
		self.cacador = None
		self.mac = "00:00:00:00:00:00"
		#self.identidade = self._get_mac()

		super(InterfaceSR, self).__init__()


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


	def _limpa_var_globais(self):
		global shared_obj
		shared_obj.set(SharedObj.MoverMovimento, Mover.PARADO)
		shared_obj.set(SharedObj.MoverHistorico, [])
		shared_obj.set(SharedObj.MoverCoordenada, self.coord_inicial)
		shared_obj.clear_event(SharedObj.MoverCoordenadaEvent)
		shared_obj.set(SharedObj.ManualMovimento, Mover.PARADO)
		shared_obj.set(SharedObj.AutomaticoValidarCaca, 0)
		shared_obj.set(SharedObj.InterfaceRespValidaCacaMsg, {})
		shared_obj.clear_event(SharedObj.InterfaceRespValidaCacaEvent)
		shared_obj.set(SharedObj.InterfaceFimJogo, 0)
		shared_obj.set(SharedObj.InterfaceCacasAtualizadas, [])
		shared_obj.set(SharedObj.InterfacePauseContinua, 0)


	def novo_jogo(self, msg):
		global shared_obj

		ret = {'cmd': MsgSRtoSS.NovoJogoConfigurado, 'ack': 0}
		if 'modo_jogo' not in msg:
			ret['erro'] = MsgRoboErro.ParametroNaoInformado
			ret['param'] = 'modo_jogo'
			return ret
		else:
			self.modo_jogo = msg['modo_jogo']

		if 'x' not in msg:
			ret['erro'] = MsgRoboErro.ParametroNaoInformado
			ret['param'] = 'x'
			return ret
		elif 'y' not in msg:
			ret['erro'] = MsgRoboErro.ParametroNaoInformado
			ret['param'] = 'y'
			return ret
		else:
			self.coord_inicial = (msg['x'], msg['y'])

		if msg['modo_jogo'] == ModoDeJogo.AUTOMATICO:
			if 'cacas' not in msg:
				ret['erro'] = MsgRoboErro.ParametroNaoInformado
				ret['param'] = 'cacas'
				return ret
			else:
				self.cacas = []
				for caca in msg['cacas']:
					self.cacas.append((caca['x'], caca['y']))

		self._limpa_var_globais()

		if self.modo_jogo == ModoDeJogo.MANUAL:
			shared_obj.set(SharedObj.ManualMovimento, Mover.PARADO)
			self.cacador = Manual(self.coord_inicial)

		elif self.modo_jogo == ModoDeJogo.AUTOMATICO:
			cacas = msg['cacas']
			self.cacador = Automatico(self.coord_inicial, self.cacas)

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
		new_cacas = []
		for caca in cacas:
			new_cacas.append((caca['x'], caca['y']))
		shared_obj.set(SharedObj.InterfaceCacasAtualizadas, new_cacas)


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
		global shared_obj
		shared_obj.set(SharedObj.TransmitirLock, msg)
		shared_obj.set_event(SharedObj.TransmitirEvent)


	def run(self):
		global shared_obj
		while True:
			# Espera alguma mensagem ...
			print("SR Aguardando mensagem \n")
			shared_obj.wait_event(SharedObj.InterfaceEvent)
			print("MENSAGEM RECEBIDA !!")

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
				resp = self.novo_jogo(msg)
				self._envia_msg(resp)

			elif cmd == MsgSStoSR.IniciaJogo:
				self.cacador.start()

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
				shared_obj.set(SharedObj.InterfaceRespValidaCacaMsg, msg)
				shared_obj.set_event(SharedObj.InterfaceRespValidaCacaEvent)

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

if __name__ == "__main__":
	t = Transmissor("localhost")
	t.start()

	r = Receptor("localhost")
	r.start()

	i = InterfaceSR()
	i.start()

	for cmd in range (1000, 1004):
		print("ENTER PARA ENVIAR MENSAGEM AO SS")
		raw_input()

		msg = {'cmd': cmd}
		shared_obj.set(SharedObj.TransmitirLock, msg)
		shared_obj.set_event(SharedObj.TransmitirEvent)

		sleep(2)

