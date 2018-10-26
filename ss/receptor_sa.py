import pika
import json
from threading import Thread
from mensagens_robo import MsgSStoSR, MsgSRtoSS, ErroMsgSStoSR
from shared_ss import *

class ReceptorSA(Thread):
	"""Recebe e trata mensagens do SA"""

	def __init__(self, host):
		super(ReceptorSA, self).__init__()

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='SA_to_SS')
		self.channel.basic_consume(self.trata_msg_recebida, queue='SA_to_SS', no_ack=True)

	def trata_msg_recebida(self, ch, method, properties, body):
		global shared_obj
		try:
			msg = json.loads(body)
		except:
			return

		msg['_dir'] = 'sa'

		shared_obj.set(SharedObj.MensagemGerente, msg)
		shared_obj.set_event(SharedObj.SolicitaGerente)


	def run(self):
		self.channel.start_consuming()