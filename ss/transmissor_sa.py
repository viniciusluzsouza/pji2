import pika
import json
from threading import Thread, Event
from shared_ss import *

class TransmissorSA(Thread):
	"""docstring for TransmissoSA"""

	def __init__(self, host):
		super(TransmissorSA, self).__init__()

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='SS_to_SA')


	def run(self):
		global shared_obj
		while True:
			# Espera ate ter uma mensagem a transmitir
			shared_obj.wait_event(SharedObj.TransmitirSAEvent)

			# Bloqueia enquanto a mensagem e enviada
			shared_obj.acquire(SharedObj.TransmitirSALock)
			msg = shared_obj.get_directly(SharedObj.TransmitirSALock)

			if '_dir' in msg: msg.pop('_dir')

			if 'robo' not in msg:
				msg['robo'] = shared_obj.get(SharedObj.NomeDoRobo)

			try:
				msg = json.dumps(msg)
				self.channel.basic_publish(exchange='', routing_key='SS_to_SA', body=msg)
			except:
				pass

			shared_obj.clear_event(SharedObj.TransmitirSAEvent)
			shared_obj.release(SharedObj.TransmitirSALock)

		self.connection.close()