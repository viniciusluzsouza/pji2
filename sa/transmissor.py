import pika
import json
from threading import Thread, Condition, Lock

transmitir_event = Event()
transmitir_msg_lock = Lock()
transmitir_msg = {}

class Transmissor(Thread):
	"""Classe transmissora de mensagens do sistema auditor."""

	def __init__(self, host):
		super(Transmissor, self).__init__()

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='SA_to_SS')


	def run(self):
		global transmitir_event, transmitir_msg_lock, transmitir_msg
		while True:
			# Espera ate ter uma mensagem a transmitir
			transmitir_event.wait()

			# Bloqueia enquanto a mensagem e enviada
			with transmitir_msg_lock:
				msg = transmitir_msg

				if '_dir' in msg: msg.pop('_dir')

				try:
					msg = json.dumps(msg)
					self.channel.basic_publish(exchange='', routing_key='SA_to_SS', body=msg)
				except:
					pass

				transmitir_event.clear()

		self.connection.close()