import zmq
from threading import Thread, Event
from shared import *

class Transmissor(object):
	"""docstring for TransmissoSR"""

	def __init__(self, host, port):
		self.context = zmq.Context()
		self.p = "tcp://" + str(host) + ":" + str(port)

		self.sock = self.context.socket(zmq.REQ)
		self.sock.bind(self.p)

		super(Transmissor, self).__init__()


		def run(self):
			global shared_obj
			while True:
				# Espera até ter uma mensagem a transmitir
				shared_obj.wait_event(SharedObj.TransmitirMsg)
				msg = shared_obj.get(SharedObj.TransmitirMsg)

				try:
					self.sock.send_json(msg)
					resp = self.sock.recv_json()
				except:
					resp = {'ack': 0, 'erro': -1}

				shared_obj.set(SharedObj.TransmitirResp, resp)
				shared_obj.set_event(SharedObj.TransmitirResp)
				shared_obj.clear_event(SharedObj.TransmitirMsg)