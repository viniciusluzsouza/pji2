import pika
import json
from threading import Thread
from mensagens_robo import MsgSStoSR, MsgSRtoSS, ErroMsgSStoSR
from shared_ss import *

class ReceptorSR(Thread):
	"""Recebe e trata mensagens do SR"""

	def __init__(self, host):
		super(ReceptorSR, self).__init__()

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='SR_to_SS')
		self.channel.basic_consume(self.trata_msg_recebida, queue='SR_to_SS', no_ack=True)

	def trata_msg_recebida(self, ch, method, properties, body):
		global shared_obj
		try:
			msg = json.loads(body)
		except:
			return

		msg['_dir'] = 'sr'

		shared_obj.set(SharedObj.MensagemGerente, msg)
		shared_obj.set_event(SharedObj.SolicitaGerente)


	def run(self):
		self.channel.start_consuming()