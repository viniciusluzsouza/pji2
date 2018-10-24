import pika
import json
from threading import Thread
from mensagens_robo import MsgSStoSR, MsgSRtoSS, ErroMsgSStoSR
from interface import *
import sys

class Receptor(Thread):
	"""Recebe e trata mensagens do SS"""

	def __init__(self, host):
		super(Receptor, self).__init__()
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='SS_to_SR')
		self.channel.basic_consume(self.trata_msg_recebida, queue='SS_to_SR', no_ack=True)

	def trata_msg_recebida(self, ch, method, properties, body):
		print("SR MENSAGEM RECEBIDA !!")
		try:
			msg = json.loads(body)
		except:
			return

		if 'cmd' not in msg:
			return

		cmd = msg['cmd']
		if cmd == MsgSStoSR.SolicitaID:
			# STUB:
			print("ID 1")

		elif cmd == MsgSStoSR.NovoJogo:
			print("NovoJogo")

		elif cmd == MsgSStoSR.Pausa:
			print("PAUSA")

		elif cmd == MsgSStoSR.FimJogo:
			print("FimJogo")

		elif cmd == MsgSStoSR.Mover:
			print("mover")

		elif cmd == MsgSStoSR.AtualizaMapa:
			print("AtualizaMapa")

		else:
			print("Comando nao reconhecido")


	def run(self):
		self.channel.start_consuming()