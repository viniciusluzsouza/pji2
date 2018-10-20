from threading import Lock, Event
from copy import deepcopy


class SharedObj(object):
	"""Manager for shared objects."""
	MoverMovimento = 0
	MoverHistorico = 1

	ManualMovimento = 10

	AutomaticoValidarCaca = 20
	AutomaticoPosicao = 21

	InterfaceFimJogo = 30
	InterfaceCacasAtualizadas = 31
	InterfacePauseContinua = 32

	TransmitirLock = 40
	TransmitirMsg = 41
	TransmitirResp = 42

	def __init__(self,):
		self.lock_dict = {
			SharedObj.MoverMovimento: Lock(),
			SharedObj.MoverHistorico: Lock(),
			SharedObj.ManualMovimento: Lock(),
			SharedObj.AutomaticoValidarCaca: Lock(),
			SharedObj.AutomaticoPosicao: Lock(),
			SharedObj.InterfaceFimJogo: Lock(),
			SharedObj.InterfaceCacasAtualizadas: Lock(),
			SharedObj.InterfacePauseContinua: Lock(),
			SharedObj.TransmitirLock: Lock(),
			SharedObj.TransmitirMsg: Event(),
			SharedObj.TransmitirResp: Event()
		}
		
		self.variables_dict = {
			SharedObj.MoverMovimento: 0,
			SharedObj.MoverHistorico: [],
			SharedObj.ManualMovimento: 0,
			SharedObj.AutomaticoValidarCaca: 0,
			SharedObj.AutomaticoPosicao: (0, 0),
			SharedObj.InterfaceFimJogo: 0,
			SharedObj.InterfaceCacasAtualizadas: [],
			SharedObj.InterfacePauseContinua: 0,
			SharedObj.TransmitirMsg: {},
			SharedObj.TransmitirResp: {}
		}

		self.acceptable = [SharedObj.MoverMovimento, SharedObj.MoverHistorico, \
		SharedObj.ManualMovimento, SharedObj.AutomaticoValidarCaca, SharedObj.AutomaticoPosicao, \
		SharedObj.InterfaceFimJogo, SharedObj.InterfaceCacasAtualizadas, SharedObj.InterfacePauseContinua, \
		SharedObj.TransmitirLock, SharedObj.TransmitirMsg, SharedObj.TransmitirResp]

	def _acceptable(self, var):
		if var not in self.acceptable:
			return False
		else:
			return True

	def wait_event(self, var):
		if not self._acceptable(var):
			return

		if type(self.lock_dict[var]) is not Event:
			return

		self.lock_dict[var].wait()

	def set_event(self, var):
		if not self._acceptable(var):
			return

		if type(self.lock_dict[var]) is not Event:
			return

		self.lock_dict[var].set()


	def clear_event(self, var):
		if not self._acceptable(var):
			return

		if type(self.lock_dict[var]) is not Event:
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
		return self.variables_dict[var]

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
