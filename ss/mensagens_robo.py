
class MsgSStoSR(object):
	"""ENUM de mensagens SS para SR"""
	SolicitaID = 1000

	NovoJogo = 1100
	Pausa = 1101
	FimJogo = 1102
	Mover = 1103

	AtualizaMapa = 1200,

class ErroMsgSStoSR(object):
	"""docstring for ErroMsgSStoS"""
	MsgFormatoInvalido = 1000
	MsgSemComando = 1001
	ComandoInvalido = 1002

	ModoNaoInformado = 1100
	CacasNaoInformadas = 1101
	CoordInicialNaoInformada = 1102

	DirecaoNaoInformada = 1200

class MsgSRtoSS(object):
	"""ENUM de mensagens de SR para SS"""
	MovendoPara = 1000
	PosicaoAtual = 1001
	ValidaCaca = 1002
	ObstaculoEncontrado = 1003

	GetPosicaoAdversario = 1100