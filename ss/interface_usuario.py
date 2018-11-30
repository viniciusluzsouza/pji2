import sys, os
from shared_ss import *
from mensagens_robo import *
from mensagens_auditor import *
from threading import Thread
from select import select

class ModoDeJogo(object):
	MANUAL = 1
	AUTOMATICO = 2

class MoverDirecao(object):
	FRENTE = 1
	DIREITA = 2
	TRAS = 3
	ESQUERDA = 4

class InterfaceUsuario(Thread):
	"""docstring for InterfaceUsuario"""
	SR_MovendoPara = 1
	SR_PosicaoAtual = 2
	SR_ValidaCaca = 3
	SA_ValidacaoCaca = 4
	SR_ObstaculoEncontrado = 5
	SA_Pausa = 6
	SA_Continua = 7
	SA_AtualizaMapa = 8

	def __init__(self):
		super(InterfaceUsuario, self).__init__()


	def inicializa_tread_evento(self):
		def func_thread_evento(manual=False):
			while True:
				global shared_obj
				shared_obj.wait_event(SharedObj.InterfaceUsuarioEvent)
				if shared_obj.get(SharedObj.InterfaceUsuarioFimJogo):
					if manual: shared_obj.set_event(SharedObj.InterfaceUsuarioNovoComando)
					break
				shared_obj.acquire(SharedObj.InterfaceUsuarioMsg)
				msg = shared_obj.get_directly(SharedObj.InterfaceUsuarioMsg)

				cmd = msg['cmd']
				if cmd == InterfaceUsuario.SR_MovendoPara:
					print("\n[SR] Movendo para: (%s, %s)" % (str(msg['x']), str(msg['y'])))

				elif cmd == InterfaceUsuario.SR_PosicaoAtual:
					print("[SR] Posicao atual: (%s, %s)" % (str(msg['x']), str(msg['y'])))
					if manual: shared_obj.set_event(SharedObj.InterfaceUsuarioNovoComando)

				elif cmd == InterfaceUsuario.SR_ValidaCaca:
					print("\n[SR-SA] Validando Caca ... ")

				elif cmd == InterfaceUsuario.SA_ValidacaoCaca:
					print("\n[SA-SR] Caca validada!! o//\n")
					if manual: shared_obj.set_event(SharedObj.InterfaceUsuarioNovoComando)

				elif cmd == InterfaceUsuario.SR_ObstaculoEncontrado:
					print("\n[SR] Obstaculo encontrado!")

				elif cmd == InterfaceUsuario.SA_Pausa:
					shared_obj.set(SharedObj.InterfaceUsuarioPausaSA, 1)
					print("\n[SA] Sistema auditor pausou o jogo!")

				elif cmd == InterfaceUsuario.SA_Continua:
					shared_obj.set(SharedObj.InterfaceUsuarioPausaSA, 0)
					print("[SA] Sistema auditor continuou o jogo!\n")

				elif cmd == InterfaceUsuario.SA_AtualizaMapa:
					print("\n[SA] Atualizacao de cacas ... \n")

				else:
					pass

				shared_obj.release(SharedObj.InterfaceUsuarioMsg)
				shared_obj.clear_event(SharedObj.InterfaceUsuarioEvent)

		if self.modo_jogo == ModoDeJogo.MANUAL:
			t = Thread(target=func_thread_evento, args=[True])
		else:
			t = Thread(target=func_thread_evento)
		t.start()


	def _novo_jogo_automatico(self):
		print("#### Serao exibidos logs na tela para monitoramento")
		print("#### digite o comando a qualquer instante.")
		print("#### Comandos: 'p' - pausa")
		print("               'c' - continua\n")

		print("Posicao inicial: %s" % str(self.posicao_inicial))
		print("Cacas: %s\n" % str(self.cacas))

		global shared_obj
		while True:
			rlist, _, _ = select([sys.stdin], [], [], 5)
			if rlist:
				if shared_obj.get(SharedObj.InterfaceUsuarioPausaSA):
					print("Sistema em pausa. Aguarde ... ")
					continue
				if shared_obj.get(SharedObj.InterfaceUsuarioFimJogo):
					print("\n#### JOGO FINALIZADO !!! ####\n")
					break

				cmd = str(sys.stdin.readline()).rstrip()
				if cmd.lower() == 'p':
					shared_obj.set(SharedObj.MensagemGerente, {'cmd': MsgSStoSR.Pausa, '_dir': 'ss'})
					shared_obj.set_event(SharedObj.SolicitaGerente)
				elif cmd.lower() == 'c':
					shared_obj.set(SharedObj.MensagemGerente, {'cmd': MsgSStoSR.Continua, '_dir': 'ss'})
					shared_obj.set_event(SharedObj.SolicitaGerente)

			if shared_obj.get(SharedObj.InterfaceUsuarioFimJogo):
				print("\n#### JOGO FINALIZADO !!! ####\n")
				break


	def _manual_valida_caca(self, x, y):
		global shared_obj
		msg = {'cmd': MsgSStoSA.ValidaCaca, 'x': x, 'y': y, '_dir': 'ss'}
		shared_obj.set(SharedObj.MensagemGerente, msg)
		shared_obj.set_event(SharedObj.SolicitaGerente)


	def _gerente_mover(self, direcao):
		global shared_obj
		if shared_obj.get(SharedObj.InterfaceUsuarioFimJogo): return
		shared_obj.set(SharedObj.MensagemGerente, {'cmd': MsgSStoSR.Mover, 'direcao': direcao, '_dir': 'ss'})
		shared_obj.set_event(SharedObj.SolicitaGerente)


	def _novo_jogo_manual(self):
		global shared_obj
		print("#### Neste modo de jogo, voce interage diretamente com o robo")
		print("#### Digite os comandos conforme orientacao a seguir:")
		print("#### Comandos: 'w' - frente")
		print("               's' - tras")
		print("               'a' - esquerda")
		print("               'd' - direita")
		print("               'v' - valida caca\n")

		print("Sua posicao inicial e: %s\n" % str(self.posicao_inicial))
		shared_obj.set_event(SharedObj.InterfaceUsuarioNovoComando)

		while True:
			shared_obj.wait_event(SharedObj.InterfaceUsuarioNovoComando, timeout=15.0)
			if shared_obj.get(SharedObj.InterfaceUsuarioFimJogo): break
			cmd = input("\n#### Digite o comando: ")

			if shared_obj.get(SharedObj.InterfaceUsuarioPausaSA):
				print("Sistema em pausa. Aguarde ... ")
				continue

			cmd = cmd.lower()
			if cmd == 'w':
				self._gerente_mover(MoverDirecao.FRENTE)
			elif cmd == 's':
				self._gerente_mover(MoverDirecao.TRAS)
			elif cmd == 'a':
				self._gerente_mover(MoverDirecao.ESQUERDA)
			elif cmd == 'd':
				self._gerente_mover(MoverDirecao.DIREITA)
			elif cmd == 'v':
				print("#### Digite sua posicao:")
				try:
					x = input("X: ")
					y = input("Y: ")
					x = int(x)
					y = int(y)
				except:
					print("Valor digitado invalido")
					continue

				if shared_obj.get(SharedObj.InterfaceUsuarioFimJogo): break
				self._manual_valida_caca(x, y)

			if shared_obj.get(SharedObj.InterfaceUsuarioFimJogo): break
			shared_obj.clear_event(SharedObj.InterfaceUsuarioNovoComando)

		print("\n#### JOGO FINALIZADO !!! ####\n")


	def novo_jogo(self, msg):
		self.modo_jogo = msg['modo_jogo']
		self.posicao_inicial = msg['posicao_inicial']

		if 'cacas' in msg:
			self.cacas = []
			for caca in msg['cacas']:
				self.cacas.append((caca['x'], caca['y']))

		self.inicializa_tread_evento()

		if self.modo_jogo == ModoDeJogo.AUTOMATICO:
			print("\n#### Modo de jogo: AUTOMATICO")
			self._novo_jogo_automatico()
		else:
			print("\n#### Modo de jogo: MANUAL")
			self._novo_jogo_manual()

		print("\nAguardando solicitacao de novo jogo do SA ... \n")


	def run(self):
		global shared_obj

		os.system('clear')
		print("###################################################")
		print("####                BEM VINDO !!!              ####")
		print("#### Interface de supervisao de robo - Grupo 3 ####")
		print("###################################################")
		print("\nAguardando solicitacao de novo jogo do SA ... \n")

		while True:
			shared_obj.wait_event(SharedObj.InterfaceUsuarioNovoJogoEvent)
			shared_obj.acquire(SharedObj.InterfaceUsuarioNovoJogoConfig)
			msg = shared_obj.get_directly(SharedObj.InterfaceUsuarioNovoJogoConfig)
			self.novo_jogo(msg)
			shared_obj.release(SharedObj.InterfaceUsuarioNovoJogoConfig)
			shared_obj.clear_event(SharedObj.InterfaceUsuarioNovoJogoEvent)