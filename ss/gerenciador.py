from threading import Thread
from shared_ss import *
from mensagens_robo import *
from mensagens_auditor import *

class ModoDeJogo(object):
	MANUAL = 1
	AUTOMATICO = 2

class Gerenciador(Thread):
	"""docstring for Gerenciador"""

	def __init__(self):
		self.jogo_em_andamento = 0
		self.modo_jogo = None

		super(Gerenciador, self).__init__()


	def _check_novo_jogo(self, msg):
		resp = {'ack': 0}
		if 'modo_jogo' not in msg:
			resp['erro'] = MsgAuditorErro.ParametroNaoInformado
			resp['param'] = 'modo_jogo'
			return resp

		if 'coord_inicial' not in msg:
			resp['erro'] = MsgAuditorErro.ParametroNaoInformado
			resp['param'] = 'coord_inicial'
			return resp

		if msg['modo_jogo'] == ModoDeJogo.AUTOMATICO \
			and 'cacas' not in msg:
			resp['erro'] = MsgAuditorErro.ParametroNaoInformado
			resp['param'] = 'cacas'

		resp['ack'] = 1
		return resp

	def sa_novo_jogo(self, msg):
		# Primeiro, verifica se os parametros estao corretos.
		# Caso nao estejam, nem envia solicitacao ao SR, envia erro ao SA
		check = self._check_novo_jogo(msg)
		if not check['ack']:
			shared_obj.set(SharedObj.TransmitirSALock, check)
			shared_obj.set_event(SharedObj.TransmitirSAEvent)
			return

		# Tudo ok, envia mensagem ao SR
		shared_obj.set(SharedObj.TransmitirSRLock, msg)
		shared_obj.clear_event(SharedObj.SolicitaGerente)
		shared_obj.set_event(SharedObj.TransmitirSREvent)

		# Ao enviar um novo jogo ao SR, a mensagem "NovoJogoConfigurado"
		# deve ser a confirmacao que o jogo foi configurado
		shared_obj.wait_event(SharedObj.SolicitaGerente)
		ack = shared_obj.get(SharedObj.MensagemGerente)
		if ack['cmd'] == MsgSRtoSS.NovoJogoConfigurado:
			# Ok, jogo configurado !!
			# Aqui podemos colocar check de posicao!!
			self.jogo_em_andamento = 1
			self.modo_jogo = msg['modo_jogo']


	def run(self):
		global shared_obj
		while True:
			# Espera alguma mensagem ...
			shared_obj.wait_event(SharedObj.SolicitaGerente)

			shared_obj.acquire(SharedObj.MensagemGerente)
			msg = shared_obj.get_directly(SharedObj.MensagemGerente)
			if 'cmd' not in msg:
				continue

			cmd = msg['cmd']

			# Solicitacoes vindas do SA
			if cmd == MsgSAtoSS.NovoJogo:
				self.sa_novo_jogo(msg)

			elif cmd == MsgSAtoSS.Pausa:
				# Avisa interface usuario
				# shared_obj.set(SharedObj.InterfaceMsg, msg)
				# shared_obj.set_event(SharedObj.InterfaceEvent)

				# Transmite para SR
				shared_obj.set(SharedObj.TransmitirSRLock, msg)
				shared_obj.set_event(SharedObj.TransmitirSREvent)

			elif cmd == MsgSAtoSS.FimJogo:
				# Transmite para SR
				shared_obj.set(SharedObj.TransmitirSRLock, msg)
				shared_obj.set_event(SharedObj.TransmitirSREvent)

			# Solicitacoes vindas do SR
			elif cmd == MsgSRtoSS.MovendoPara:
				print("MOVENDO PARA")
				# # Avisa interface usuario
				# shared_obj.set(SharedObj.InterfaceMsg, msg)
				# shared_obj.set_event(SharedObj.InterfaceEvent)

				# # Transmite para SA
				shared_obj.set(SharedObj.TransmitirSALock, msg)
				shared_obj.set_event(SharedObj.TransmitirSAEvent)

			elif cmd == MsgSRtoSS.PosicaoAtual:
				print("POSICAO ATUAL")
				# shared_obj.set(SharedObj.InterfaceMsg, msg)
				# shared_obj.set_event(SharedObj.InterfaceEvent)
				shared_obj.set(SharedObj.TransmitirSALock, msg)
				shared_obj.set_event(SharedObj.TransmitirSAEvent)

			elif cmd == MsgSRtoSS.ValidaCaca:
				print("VALIDA CACA")
				# shared_obj.set(SharedObj.InterfaceMsg, msg)
				# shared_obj.set_event(SharedObj.InterfaceEvent)
				shared_obj.set(SharedObj.TransmitirSALock, msg)
				shared_obj.set_event(SharedObj.TransmitirSAEvent)

			elif cmd == MsgSRtoSS.ObstaculoEncontrado:
				print("OBSTACULO ENCONTRADO")
				# shared_obj.set(SharedObj.InterfaceMsg, msg)
				# shared_obj.set_event(SharedObj.InterfaceEvent)
				shared_obj.set(SharedObj.TransmitirSALock, msg)
				shared_obj.set_event(SharedObj.TransmitirSAEvent)

			else:
				pass

			shared_obj.release(SharedObj.MensagemGerente)
			shared_obj.clear_event(SharedObj.SolicitaGerente)

