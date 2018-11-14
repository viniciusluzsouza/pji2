import pika
import json
from threading import Thread, Event, Lock
import compartilhados

class Transmissor(Thread):
	"""Classe transmissora de mensagens do sistema auditor."""

	def __init__(self, host):
		super(Transmissor, self).__init__()

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='SA_to_SS')


	def run(self):
		while True:
			# Espera ate ter uma mensagem a transmitir
			compartilhados.transmitir_event.wait()

			# Bloqueia enquanto a mensagem e enviada
			with compartilhados.transmitir_msg_lock:
				msg = compartilhados.transmitir_msg

				if '_dir' in msg: msg.pop('_dir')

				print("Enviando: %s" % str(msg))

				try:
					msg = json.dumps(msg)
					self.channel.basic_publish(exchange='', routing_key='SA_to_SS', body=msg)
				except:
					pass

				compartilhados.transmitir_event.clear()

		self.connection.close()