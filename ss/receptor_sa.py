import pika
import json
from threading import Thread
from mensagens_robo import MsgSStoSR, MsgSRtoSS, ErroMsgSStoSR
from shared_ss import *

class ReceptorSA(Thread):
	"""Recebe e trata mensagens do SA"""

	def __init__(self, host):
		global shared_obj
		super(ReceptorSA, self).__init__()
		self._nome = shared_obj.get(SharedObj.NomeDoRobo)
		self._exchange = 'SA_to_SS'

		# credenciais = pika.PlainCredentials('test', 'test')
		# self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host), credentials=credenciais))
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange=self._exchange, exchange_type='direct')

		result = self.channel.queue_declare(exclusive=True)
		self._queue_name = result.method.queue

		self.channel.queue_bind(exchange=self._exchange, queue=self._queue_name, routing_key=self._nome)
		self.channel.queue_bind(exchange=self._exchange, queue=self._queue_name, routing_key='cadastro')

		self.channel.basic_consume(self.trata_msg_recebida, queue=self._queue_name, no_ack=True)


	def _atualiza_nome(self, nome):
		self._nome = nome
		self.channel.queue_bind(exchange=self._exchange, queue=self._queue_name, routing_key=self._nome)


	def trata_msg_recebida(self, ch, method, properties, body):
		global shared_obj

		try:
			msg = json.loads(body)
		except:
			return

		if method.routing_key == 'cadastro':
			if 'nome' in msg: self._atualiza_nome(msg['nome'])

		msg['_dir'] = 'sa'

		shared_obj.set(SharedObj.MensagemGerente, msg)
		shared_obj.set_event(SharedObj.SolicitaGerente)


	def run(self):
		self.channel.start_consuming()

