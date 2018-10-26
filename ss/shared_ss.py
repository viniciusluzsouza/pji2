from threading import Lock, Event
from copy import deepcopy


class SharedObj(object):
	"""Manager for shared objects."""
	SolicitaGerente = 1
	MensagemGerente = 2
	RespostaGerente = 3

	InterfaceEvent = 10
	InterfaceMsg = 11

	TransmitirSALock = 30
	TransmitirSAEvent = 31

	TransmitirSRLock = 40
	TransmitirSREvent = 41

	InterfaceUsuarioEvent = 50
	InterfaceUsuarioMsg = 51
	InterfaceUsuarioFimJogo = 52
	InterfaceUsuarioNovoJogoEvent = 53
	InterfaceUsuarioNovoJogoConfig = 54

	def __init__(self,):
		self.lock_dict = {
			SharedObj.SolicitaGerente: Event(),
			SharedObj.MensagemGerente: Lock(),

			SharedObj.InterfaceEvent: Event(),
			SharedObj.InterfaceMsg: Lock(),
			SharedObj.RespostaGerente: Lock(),

			SharedObj.TransmitirSALock: Lock(),
			SharedObj.TransmitirSAEvent: Event(),

			SharedObj.TransmitirSRLock: Lock(),
			SharedObj.TransmitirSREvent: Event(),

			SharedObj.InterfaceUsuarioMsg: Lock(),
			SharedObj.InterfaceUsuarioEvent: Event(),
			SharedObj.InterfaceUsuarioFimJogo: Lock(),
			SharedObj.InterfaceUsuarioNovoJogoEvent: Event(),
			SharedObj.InterfaceUsuarioNovoJogoConfig: Lock(),
		}
		
		self.variables_dict = {
			SharedObj.MensagemGerente: {},
			SharedObj.RespostaGerente: {},

			SharedObj.InterfaceMsg: {},

			SharedObj.TransmitirSALock: {},

			SharedObj.TransmitirSRLock: {},
			SharedObj.InterfaceUsuarioMsg: {},
			SharedObj.InterfaceUsuarioFimJogo: 0,
			SharedObj.InterfaceUsuarioNovoJogoConfig: {}
		}

		self.acceptable = [ SharedObj.SolicitaGerente, SharedObj.MensagemGerente, SharedObj.RespostaGerente, \
		SharedObj.TransmitirSALock, SharedObj.TransmitirSAEvent, SharedObj.TransmitirSRLock, SharedObj.TransmitirSREvent, \
		SharedObj.InterfaceUsuarioMsg, SharedObj.InterfaceUsuarioEvent, SharedObj.InterfaceUsuarioFimJogo, \
		SharedObj.InterfaceUsuarioNovoJogoEvent, SharedObj.InterfaceUsuarioNovoJogoConfig]

	def _acceptable(self, var):
		if var not in self.acceptable:
			return False
		else:
			return True

	def wait_event(self, var):
		if not self._acceptable(var):
			return

		self.lock_dict[var].wait()

	def set_event(self, var):
		if not self._acceptable(var):
			return

		self.lock_dict[var].set()


	def clear_event(self, var):
		if not self._acceptable(var):
			return

		self.lock_dict[var].clear()


	def set(self, var, value):
		if not self._acceptable(var):
			return

		self.lock_dict[var].acquire()
		self.variables_dict[var] = deepcopy(value)
		self.lock_dict[var].release()

	def set_directly(self, var, val):
		self.variables_dict[var] = deepcopy(val)

	def get(self, var):
		if not self._acceptable(var):
			return

		self.lock_dict[var].acquire()
		ret = deepcopy(self.variables_dict[var])
		self.lock_dict[var].release()
		return ret

	def get_directly(self, var):
		return deepcopy(self.variables_dict[var])

	def acquire(self, var):
		if not self._acceptable(var):
			return False

		self.lock_dict[var].acquire()
		return True

	def release(self, var):
		if not self._acceptable(var):
			return

		self.lock_dict[var].release()
		return 1

	def append_list(self, var, val):
		ret = True
		self.acquire(var)
		if type(self.variables_dict[var]) is not list:
			ret = False
		else:
			self.variables_dict[var].append(val)

		self.release(var)
		return ret

# Singleton object for shared objects
shared_obj = SharedObj()
