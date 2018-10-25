
class MsgSAtoSS(object):
	"""ENUM de mensagens SS para SR"""
	SolicitaID = 1000

	NovoJogo = 1100
	Pausa = 1101
	FimJogo = 1102

	AtualizaMapa = 1200

	ValidacaoCaca = 2000


class MsgSStoSA(object):
	"""ENUM de mensagens de SR para SS"""
	MovendoPara = 1000
	PosicaoAtual = 1001
	ValidaCaca = 1002
	ObstaculoEncontrado = 1003


class MsgAuditorErro(object):
	"""docstring for ErroMsgSStoS"""
	MsgFormatoInvalido = 1000
	MsgSemComando = 1001
	ComandoInvalido = 1002
	ParametroNaoInformado = 1003