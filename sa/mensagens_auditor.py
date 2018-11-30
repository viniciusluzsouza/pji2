
class MsgSAtoSS(object):
	"""ENUM de mensagens SS para SR"""
	CadastraRobo = 1000
	SolicitaID = 1001
	SolicitaHistorico = 1002
	SolicitaStatus = 1003

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
	SolicitaStatus_RESP = 2003

class MsgAuditorErro(object):
	"""docstring for ErroMsgSStoS"""
	MsgFormatoInvalido = 1000
	MsgSemComando = 1001
	ComandoInvalido = 1002
	ParametroNaoInformado = 1003

class MsgAuditorToUI(object):
	"""docstring for MsgAuditorToUI"""
	AtualizarRobo = 3001
	ValidarCaca = 3003
	Obstaculo = 3004
	SolicitaID_REP = 3005
	RecuperarHistorico_RESP = 3006
	SolicitaStatus_RESP = 3007
	RecuperarCadastro = 3008
	DeclararVencedor = 3030

class MsgUItoAuditor(object):
	"""docstring for MsgUItoAuditor"""
	FimdeJogo = 4000
	RecuperarHistorico = 4001
	CadastrarRobo = 4002
	RecuperarCadastros = 4003
	ValidarCaca = 4004
	NovoJogo = 4005



