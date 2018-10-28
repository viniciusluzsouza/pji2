from threading import Thread
from time import sleep
import pika
import json

def receptor():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='SS_to_SA')

	def responde(msg):
		print("respondendo: %s" % str(msg))
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()
		channel.queue_declare(queue='SA_to_SS')
		channel.basic_publish(exchange='', routing_key='SA_to_SS', body=json.dumps(msg))
		connection.close()

	def callback(ch, method, properties, body):
		print("SA Recebeu: %s" % str(body))
		try:
			msg = json.loads(body)
			if msg['cmd'] == 1002:
				responde({'cmd': 2000, 'ack': 1})	# msg valida caca
		except:
			pass

	channel.basic_consume(callback, queue='SS_to_SA', no_ack=True)
	channel.start_consuming()


if __name__ == '__main__':
	consumidor = Thread(target=receptor)
	consumidor.start()

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='SA_to_SS')

	while True:
		print(" ### Escolha a opcao de mensagem:")
		print("1) Novo jogo manual")
		print("2) Novo jogo automatico")
		print("3) Pause")
		print("4) Continua")
		print("5) Fim do Jogo")
		print("6) Atualiza mapa")
		print("7) Solicita ID")
		print("8) Solicita Historico")
		print("9) Cadastra Robo")
		print("10) Solicita Status")
		print("\n0) Sair")

		op = input("Opcao: ")
		try:
			op = int(op)
			if op == 1:
				msg = {'cmd': 1100, 'modo_jogo': 1, 'x': 0, 'y': 0}
			elif op == 2:
				cacas = []
				cacas.append({'x': 5, 'y': 3})
				cacas.append({'x': 1, 'y': 2})
				cacas.append({'x': 3, 'y': 4})
				cacas.append({'x': 6, 'y': 1})
				cacas.append({'x': 2, 'y': 1})
				msg = {'cmd': 1100, 'modo_jogo': 2, 'x': 0, 'y': 0, 'cacas': cacas}
			elif op == 3:
				msg = {'cmd': 1101}
			elif op == 4:
				msg = {'cmd': 1102}
			elif op == 5:
				msg = {'cmd': 1103}
			elif op == 6:
				cacas = []
				# cacas.append({'x': 5, 'y': 3})
				cacas.append({'x': 1, 'y': 2})
				cacas.append({'x': 3, 'y': 4})
				cacas.append({'x': 2, 'y': 1})
				msg = {'cmd': 1200, 'cacas': cacas}
			elif op == 7:
				msg = {'cmd': 1001}
			elif op == 8:
				msg = {'cmd': 1002}
			elif op == 9:
				cor = input("Digite a cor: ")
				nome = input("Digite o nome: ")
				msg = {'cmd': 1000, 'cor': cor, 'nome': nome}
			elif op == 10:
				msg = {'cmd': 1003}
			elif op == 0:
				break
		except:
			print("Opcao invalida")
			continue

		channel.basic_publish(exchange='', routing_key='SA_to_SS', body=json.dumps(msg))
		sleep(2)