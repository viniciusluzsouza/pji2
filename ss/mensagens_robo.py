
class MsgSStoSR(object):
	"""ENUM de mensagens SS para SR"""
	CadastraRobo = 1000
	SolicitaID = 1001
	SolicitaHistorico = 1002
	SolicitaStatus = 1003

	NovoJogo = 1100
	Pausa = 1101
	Continua = 1102
	FimJogo = 1103
	Mover = 1104
	IniciaJogo = 1105

	AtualizaMapa = 1200

	ValidacaoCaca = 2000

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

	SolicitaID_Resp = 2000
	NovoJogoConfigurado = 2001
	SolicitaHistorico_RESP = 2002
	SolicitaStatus_RESP = 2003
	FinalizaJogo = 2004

class MsgRoboErro(object):
	"""docstring for ErroMsgSStoS"""
	MsgFormatoInvalido = 1000
	MsgSemComando = 1001
	ComandoInvalido = 1002
	ParametroNaoInformado = 1003