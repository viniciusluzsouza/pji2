from threading import Thread
from time import sleep
import pika
import json

def receptor():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='SS_to_SA')

	def callback(ch, method, properties, body):
		print("SA Recebeu: %s" % str(body))

	channel.basic_consume(callback, queue='SS_to_SA', no_ack=True)
	channel.start_consuming()


if __name__ == '__main__':
	consumidor = Thread(target=receptor)
	consumidor.start()

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='SA_to_SS')

	for cmd in range(1100, 1103):
		print("ENTER PARA ENVIAR MENSAGEM AO SS")
		raw_input()

		msg = {'cmd': cmd}
		channel.basic_publish(exchange='', routing_key='SA_to_SS', body=json.dumps(msg))

		sleep(2)