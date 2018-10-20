import zmq
from threading import Thread
from mensagens_robo import MsgSStoSR, MsgSRtoSS, ErroMsgSStoSR
from interface import InterfaceSR, ModoDeJogo

class Receptor(Thread):
	"""Recebe e trata mensagens do SR"""

	def __init__(self, port, interface):
		self.interface = interface
		self.context = zmq.Context()
		self.p = "tcp://*:" + str(port)

		self.sock = self.context.socket(zmq.REP)
		self.sock.bind(self.p)

		super(Receptor, self).__init__()
		

		def _criar_msg_sucesso(self):
			return {'ack': 1}

		def _criar_msg_erro(self, erro):
			return {'ack': 0, 'erro': erro}

		def _trata_msg_novo_jogo(self, msg):
			if 'modo' not in msg:
				return -1, ErroMsgSStoSR.ModoNaoInformado

			if 'coord_inicial' not in msg:
				return -1, ErroMsgSStoSR.CoordInicialNaoInformada

			modo = msg['modo']
			if modo == ModoDeJogo.AUTOMATICO and \
				('cacas' not in msg or not len(msg['cacas'])):
				return -1, ErroMsgSStoSR.CacasNaoInformadas

			cacas = msg['cacas'] if 'cacas' in msg else None
			self.interface.novo_jogo(modo=modo, coord_inicial=coord_inicial, cacas=cacas)
			return 0, 0

		def run(self):
			while True:
				try:
					msg = self.sock.recv_json()
				except:
					self.sock.send_json(self._criar_msg_erro(ErroMsgSStoSR.MsgFormatoInvalido))
					continue


				if 'cmd' not in msg:
					self.sock.send_json(self._criar_msg_erro(ErroMsgSStoSR.MsgSemComando))
					continue

				ret = self._criar_msg_sucesso()
				cmd = msg['cmd']
				if cmd == MsgSStoSR.SolicitaID:
					ret['buffer'] = self.interface.get_identidade()

				elif cmd == MsgSStoSR.NovoJogo:
					# modo, coord_inicial, cacas=None
					r, e = self._trata_msg_novo_jogo(msg)
					if r < 0:
						ret.update(self._criar_msg_erro(e))

				elif cmd == MsgSStoSR.Pausa:
					self.interface.pause()

				elif cmd == MsgSStoSR.FimJogo:
					self.interface.fim_jogo()

				elif cmd == MsgSStoSR.Mover:
					if 'direcao' not in msg:
						ret.update(self._criar_msg_erro(ErroMsgSStoSR.DirecaoNaoInformada))
					else:
						self.interface.mover_manual(msg['direcao'])

				elif cmd == MsgSStoSR.AtualizaMapa:
					pass

				else:
					ret.update(self._criar_msg_erro(ErroMsgSStoSR.ComandoInvalido))

				self.sock.send_json(ret)
				

