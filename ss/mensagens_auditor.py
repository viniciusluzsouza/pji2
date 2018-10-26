
class MsgSAtoSS(object):
	"""ENUM de mensagens SS para SR"""
	SolicitaID = 1000
	SolicitaHistorico = 1001

	NovoJogo = 1100
	Pausa = 1101
	Continua = 1102
	FimJogo = 1103

	AtualizaMapa = 1200

	ValidacaoCaca = 2000


class MsgSStoSA(object):
	"""ENUM de mensagens de SR para SS"""
	MovendoPara = 1000
	PosicaoAtual = 1001
	ValidaCaca = 1002
	ObstaculoEncontrado = 1003

	SolicitaID_Resp = 2000
	SolicitaHistorico_RESP = 2002

class MsgAuditorErro(object):
	"""docstring for ErroMsgSStoS"""
	MsgFormatoInvalido = 1000
	MsgSemComando = 1001
	ComandoInvalido = 1002
	ParametroNaoInformado = 1003