import pika
import json
from threading import Thread, Event
from shared_ss import *

class TransmissorSR(Thread):
	"""docstring for TransmissoSR"""

	def __init__(self, host):
		super(TransmissorSR, self).__init__()

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='SS_to_SR')


	def run(self):
		global shared_obj
		while True:
			# Espera ate ter uma mensagem a transmitir
			shared_obj.wait_event(SharedObj.TransmitirSREvent)

			# Bloqueia enquanto a mensagem e enviada
			shared_obj.acquire(SharedObj.TransmitirSRLock)
			msg = shared_obj.get_directly(SharedObj.TransmitirSRLock)

			if '_dir' in msg: msg.pop('_dir')

			msg_prop = None
			if '_ttl' in msg:
				msg_prop = pika.BasicProperties(expiration=str(msg['_ttl']))
				msg.pop('_ttl')

			try:
				msg = json.dumps(msg)
				self.channel.basic_publish(exchange='', routing_key='SS_to_SR', body=msg, properties=msg_prop)
			except:
				pass

			shared_obj.clear_event(SharedObj.TransmitirSREvent)
			shared_obj.release(SharedObj.TransmitirSRLock)

		self.connection.close()