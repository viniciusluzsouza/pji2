from threading import Thread
from shared_ss import *
from mensagens_robo import *
from mensagens_auditor import *
from interface_usuario import *
import json

class Gerenciador(Thread):
	"""docstring for Gerenciador"""

	def __init__(self):
		self.jogo_em_andamento = 0
		self.modo_jogo = None
		self.intf_usuario = InterfaceUsuario()
		self._ler_cadastro()

		super(Gerenciador, self).__init__()


	def _check_novo_jogo(self, msg):
		resp = {'ack': 0}
		if 'modo_jogo' not in msg:
			resp['erro'] = MsgAuditorErro.ParametroNaoInformado
			resp['param'] = 'modo_jogo'
			return resp

		if 'x' not in msg:
			resp['erro'] = MsgAuditorErro.ParametroNaoInformado
			resp['param'] = 'x'
			return resp

		if 'y' not in msg:
			resp['erro'] = MsgAuditorErro.ParametroNaoInformado
			resp['param'] = 'y'
			return resp

		if msg['modo_jogo'] == ModoDeJogo.AUTOMATICO \
			and 'cacas' not in msg:
			resp['erro'] = MsgAuditorErro.ParametroNaoInformado
			resp['param'] = 'cacas'

		resp['ack'] = 1
		return resp

	def sa_novo_jogo(self, msg):
		global shared_obj
		# Primeiro, verifica se os parametros estao corretos.
		# Caso nao estejam, nem envia solicitacao ao SR, envia erro ao SA
		check = self._check_novo_jogo(msg)
		if not check['ack']:
			shared_obj.set(SharedObj.TransmitirSALock, check)
			shared_obj.set_event(SharedObj.TransmitirSAEvent)
			return

		# Tudo ok, envia mensagem ao SR
		msg['_ttl'] = 10
		shared_obj.set(SharedObj.TransmitirSRLock, msg)
		shared_obj.release(SharedObj.MensagemGerente)
		shared_obj.clear_event(SharedObj.SolicitaGerente)
		shared_obj.set_event(SharedObj.TransmitirSREvent)

		# Ao enviar um novo jogo ao SR, a mensagem "NovoJogoConfigurado"
		# deve ser a confirmacao que o jogo foi configurado
		shared_obj.wait_event(SharedObj.SolicitaGerente, timeout=10.0)
		shared_obj.acquire(SharedObj.MensagemGerente)

		if not shared_obj.is_set(SharedObj.SolicitaGerente):
			# Aconteceu timeout
			print("--> SA tentou iniciar jogo, porem SR nao responde.")
			return

		ack = shared_obj.get_directly(SharedObj.MensagemGerente)
		if ack['cmd'] == MsgSRtoSS.NovoJogoConfigurado:
			# Ok, jogo configurado !!
			# Aqui podemos colocar check de posicao!!
			self.jogo_em_andamento = 1
			self.modo_jogo = msg['modo_jogo']
			ui_msg = {'modo_jogo': self.modo_jogo, 'posicao_inicial': (msg['x'], msg['y'])}
			if 'cacas' in msg: ui_msg['cacas'] = msg['cacas']

			# Avisa interface usuario
			shared_obj.set(SharedObj.InterfaceUsuarioFimJogo, 0)
			shared_obj.set(SharedObj.InterfaceUsuarioNovoJogoConfig, ui_msg)
			shared_obj.set_event(SharedObj.InterfaceUsuarioNovoJogoEvent)

			# Inicia jogo IniciaJogo
			shared_obj.clear_event(SharedObj.TransmitirSREvent)
			shared_obj.set(SharedObj.TransmitirSRLock, {'cmd': MsgSStoSR.IniciaJogo})
			shared_obj.set_event(SharedObj.TransmitirSREvent)

	def _ler_cadastro(self):
		global shared_obj
		try:
			with open('cadastro.cfg') as f:
				cadastro = json.load(f)
				self.cor = cadastro['cor']
				self.nome = cadastro['nome']
				self.mac = cadastro['mac']
		except:
			self.cor = 0
			self.nome = "Grupo3"
			self.mac = "00:00:00:00:00:00"

		shared_obj.set(SharedObj.NomeDoRobo, self.nome)

	def _atualiza_cadastro(self):
		global shared_obj
		shared_obj.set(SharedObj.NomeDoRobo, self.nome)
		cadastro = {'cor': self.cor, 'nome': self.nome, 'mac': self.mac}
		with open('cadastro.cfg', 'w') as f:
			json.dump(cadastro, f)

	def cadastra_robo(self, msg):
		if 'cor' not in msg:
			return

		self.cor = msg['cor']
		self.nome = msg['nome'] if 'nome' in msg else 'Grupo3'
		self.mac = msg['mac'] if 'mac' in msg else '00:00:00:00:00:00'
		self._atualiza_cadastro()

	def run(self):
		global shared_obj
		self.intf_usuario.start()
		
		while True:
			# Espera alguma mensagem ...
			shared_obj.wait_event(SharedObj.SolicitaGerente)

			shared_obj.acquire(SharedObj.MensagemGerente)
			msg = shared_obj.get_directly(SharedObj.MensagemGerente)
			if 'cmd' not in msg:
				shared_obj.clear_event(SharedObj.SolicitaGerente)
				continue

			cmd = msg['cmd']

			# Solicitacoes vindas do SA
			if '_dir' in msg and msg['_dir'] == 'sa':
				if cmd == MsgSAtoSS.NovoJogo:
					self.sa_novo_jogo(msg)

				elif cmd == MsgSAtoSS.SolicitaID:
					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.Pausa:
					# Avisa interface usuario
					ui_msg = {'cmd': InterfaceUsuario.SA_Pausa}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.Continua:
					# Avisa interface usuario
					ui_msg = {'cmd': InterfaceUsuario.SA_Continua}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.FimJogo:
					# Avisa interface usuario
					shared_obj.set(SharedObj.InterfaceUsuarioFimJogo, 1)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.ValidacaoCaca:
					# Avisa interface usuario
					ui_msg = {'cmd': InterfaceUsuario.SA_ValidacaoCaca}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.AtualizaMapa:
					# Avisa interface usuario
					ui_msg = {'cmd': InterfaceUsuario.SA_AtualizaMapa, 'cacas': msg['cacas']}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.SolicitaHistorico:
					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.CadastraRobo:
					self.cadastra_robo(msg)

					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSAtoSS.SolicitaStatus:
					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				else:
					pass

			# Solicitacoes vindas do SR
			elif '_dir' in msg and msg['_dir'] == 'sr':
				if cmd == MsgSRtoSS.SolicitaID_Resp:
					# Transmite para SA
					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSRtoSS.MovendoPara:
					# Avisa interface usuario
					ui_msg = {'cmd': InterfaceUsuario.SR_MovendoPara, 'x': msg['x'], 'y': msg['y']}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					# Transmite para SA
					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSRtoSS.PosicaoAtual:
					ui_msg = {'cmd': InterfaceUsuario.SR_PosicaoAtual, 'x': msg['x'], 'y': msg['y']}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSRtoSS.ValidaCaca:
					ui_msg = {'cmd': InterfaceUsuario.SR_ValidaCaca}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSRtoSS.ObstaculoEncontrado:
					ui_msg = {'cmd': InterfaceUsuario.SR_ObstaculoEncontrado}
					shared_obj.set(SharedObj.InterfaceUsuarioMsg, ui_msg)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSRtoSS.SolicitaHistorico_RESP:
					# Transmite para SA
					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSRtoSS.SolicitaStatus_RESP:
					# Transmite para SA
					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSRtoSS.FinalizaJogo:
					# Avisa interface usuario
					shared_obj.set(SharedObj.InterfaceUsuarioFimJogo, 1)
					shared_obj.set_event(SharedObj.InterfaceUsuarioEvent)

				else:
					pass

			# Solicitacoes vindas do proprio ss
			elif '_dir' in msg and msg['_dir'] == 'ss':
				if cmd == MsgSStoSR.Mover:
					# Transmite para SR
					msg['_ttl'] = 5000
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

				elif cmd == MsgSStoSA.ValidaCaca:
					# Transmite para SA
					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

				elif cmd == MsgSStoSR.Pausa \
					or MsgSStoSR.Continua:
					# Transmite para SR
					shared_obj.set(SharedObj.TransmitirSRLock, msg)
					shared_obj.set_event(SharedObj.TransmitirSREvent)

					# Transmite para SA
					shared_obj.set(SharedObj.TransmitirSALock, msg)
					shared_obj.set_event(SharedObj.TransmitirSAEvent)

			shared_obj.release(SharedObj.MensagemGerente)
			shared_obj.clear_event(SharedObj.SolicitaGerente)

