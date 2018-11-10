from threading import Thread, Lock, Event
from mensagens_auditor import *

solicita_gerente = Event()
gerente_msg_lock = Lock()
gerente_msg = {}

class Gerenciador(Thread):
	"""Gerenciador do SA. Trata mensagens vindas de qualquer lugar."""

	def __init__(self):
		super(Gerenciador, self).__init__()

	def run(self):
		global solicita_gerente, gerente_msg_lock, gerente_msg

		while True:
			# Espera alguma mensagem ...
			solicita_gerente.wait()

			with gerente_msg_lock:
				msg = gerente_msg

				if 'cmd' not in msg:
					solicita_gerente.clear()
					continue

				cmd = msg['cmd']

				# Solicitacoes vindas do SS
				if '_dir' in msg and msg['_dir'] == 'sa':
					if cmd == MsgSStoSA.MovendoPara:
						# Avisa interface usuario

					elif cmd == MsgSStoSA.PosicaoAtual:
						# Avisa interface usuario

					elif cmd == MsgSStoSA.ValidaCaca:
						# Avisa interface usuario

					elif cmd == MsgSStoSA.ObstaculoEncontrado:
						# Avisa interface usuario

					elif cmd == MsgSStoSA.SolicitaID_Resp:
						# Avisa interface usuario

					elif cmd == MsgSStoSA.SolicitaHistorico_RESP:
						# Avisa interface usuario

					elif cmd == MsgSStoSA.SolicitaStatus_RESP:
						# Avisa interface usuario

					else:
						# Comando nao identificado, nao faz nada ...
						pass

				# Solicitacoes vindas da interface de usuario
				elif '_dir' in msg and msg['_dir'] == 'ui':
					'''
					Sugestao: as classes interface usuario e principal
					podem se comunicar com o gerente da mesma forma que
					o SS se comunica com o SA (atraves de mensagens JSON).
					Isto deve facilitar a implementacao, pois ja temos
					o cenario montado, basta criar os IF's ...

					if cmd == MsgUItoGerente.NovoJogo:
						# Transmite para SS

					elif ...
					'''

				# Solicitacoes vindas da classe principal
				elif '_dir' in msg and msg['_dir'] == 'pr':
					# Aqui podemos fazer da mesma forma ...

				solicita_gerente.clear()




