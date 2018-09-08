from ev3dev.ev3 import *
from time import time, sleep
from threading import Thread, Lock

mutexMovimento = Lock()
movimento = 0

def verifica_mutex_movimento():
	global movimento
	mutexMovimento.acquire()
	ret = movimento
	mutexMovimento.release()
	return ret

def seta_mutex_movimento(val):
	global movimento
	mutexMovimento.acquire()
	movimento = val
	mutexMovimento.release()

class Cor(object):
	# 0=unknown, 1=black, 2=blue, 3=green, 4=yellow, 5=red, 6=white, 7=brown
	INDEFINIDO = 0
	PRETO = 1
	AZUL = 2
	VERDE = 3
	AMARELO = 4
	VERMELHO = 5
	BRANCO = 6
	MARROM = 7

	corToString = {
		INDEFINIDO: 'indefinido',
		PRETO: 'preto',
		AZUL: 'azul',
		VERDE: 'verde',
		AMARELO: 'amarelo',
		VERMELHO: 'vermelho',
		BRANCO: 'branco',
		MARROM: 'marrom'
	}


class Mover(Thread):
	"""docstring for Mover"""
	EXIT = -1
	PARADO = 0
	FRENTE = 1
	DIREITA = 2
	TRAS = 3
	ESQUERDA = 4

	def __init__(self, x, y):
		self.status = 0
		self.motor_direita = Motor(OUTPUT_C)
		self.motor_esquerda = Motor(OUTPUT_B)
		self.sensor_us = UltrasonicSensor()
		self.sensor_luminosidade = ColorSensor()

		# Configura modo dos sensores
		self.sensor_luminosidade.mode = 'COL-REFLECT'
		self.sensor_us.mode = 'US-DIST-CM'
		# assert cl.connected, "Connect a color sensor to any sensor port"

		# Atributos ocultos
		self._ultima_direcao = Mover.FRENTE
		self._min_ref = 5
		self._max_ref = 80
		self._pause = False
		self._coord_ini = (x, y)
		self._coord_x = x
		self._coord_y = y
		self._next_coord = (x, y)

		super(Mover, self).__init__()


	def calibra_girando(self):
		"""Calibra fazendo meia volta e retornando a posicao original"""
		speed = 150
		for i in range(0, 2):
			self.motor_direita.run_forever(speed_sp=speed)
			end_time = time() + 2
			while time() < end_time:
				read = self.sensor_luminosidade.value()
				if self._max_ref < read:
					self._max_ref = read
				if self._min_ref > read:
					self._min_ref = read
			self.motor_direita.stop()
			speed -= 290


	def calibra_andando(self):
		"""Calibra já andando pra frente"""
		self.sensor_luminosidade.mode = 'COL-REFLECT'
		self.motor_esquerda.run_direct(duty_cycle_sp=30)
		self.motor_direita.run_direct(duty_cycle_sp=30)
		self._max_ref = 0
		self._min_ref = 100
		end_time = time() + 5
		while time() < end_time:
			read = self.sensor_luminosidade.value()
			if self._max_ref < read:
				self._max_ref = read
			if self._min_ref > read:
				self._min_ref = read


	def get_status(self):
		"""Retorna o status do robo:
			0 - parado
			1 - andando """
		return self.status

	def _encontra_faixa(self, encontra_faixa_esquerda=False):
		self.sensor_luminosidade.mode = 'COL-COLOR'

		if self.sensor_luminosidade.value() == Cor.PRETO:
			return

		vel = 100
		if encontra_faixa_esquerda:
			self.motor_esquerda.run_timed(time_sp=500, speed_sp=vel)
			end_time = time() + 0.5
			while time() < end_time:
				if self.sensor_luminosidade.value() == Cor.PRETO:
					self.stop()
					return

			self.stop()
			self.motor_esquerda.run_timed(time_sp=500, speed_sp=-vel)
			self.motor_direita.run_timed(time_sp=500, speed_sp=2*vel)
			end_time = time() + 0.5
			while time() < end_time:
				if self.sensor_luminosidade.value() == Cor.PRETO:
					sleep(0.2)
					self.stop()
					return
		else:
			self.motor_direita.run_timed(time_sp=500, speed_sp=vel)
			end_time = time() + 0.5
			while time() < end_time:
				if self.sensor_luminosidade.value() == Cor.PRETO:
					self.stop()
					return

			self.stop()
			self.motor_direita.run_timed(time_sp=500, speed_sp=-vel)
			self.motor_esquerda.run_timed(time_sp=500, speed_sp=2*vel)
			end_time = time() + 0.5
			while time() < end_time:
				if self.sensor_luminosidade.value() == Cor.PRETO:
					sleep(0.2)
					self.stop()
					return


	def _calc_next_coord(self, direcao, coord=None):
		coord_x = self._coord_x
		coord_y = self._coord_y

		if coord is not None:
			coord_x = coord[0]
			coord_y = coord[1]

		if self._coord_ini == (0, 0):
			if direcao == Mover.FRENTE:
				coord_y += 1
			elif direcao == Mover.DIREITA:
				coord_x += 1
			elif direcao == Mover.TRAS:
				coord_y -= 1
			elif direcao == Mover.ESQUERDA:
				coord_x -= 1

		elif self._coord_ini == (6, 6):
			if direcao == Mover.FRENTE:
				coord_y -= 1
			elif direcao == Mover.DIREITA:
				coord_x -= 1
			elif direcao == Mover.TRAS:
				coord_y += 1
			elif direcao == Mover.ESQUERDA:
				coord_x += 1

		return (coord_x, coord_y)

	def _finalizar_movimento(self):
		global movimento
		self.stop()
		mutexMovimento.acquire()
		if movimento != Mover.EXIT:
			movimento = Mover.PARADO
		mutexMovimento.release()


	def move(self, direcao, coord_atual=None):
		"""Move em uma direcao (frente, direita, esquerda, tras).
			Se for passada a mesma direcao, calibra e segue em fente"""

		if direcao == Mover.PARADO or direcao == Mover.EXIT:
			self.stop()
			return

		calc_coord = self._calc_next_coord(direcao, coord_atual)
		self._next_coord = calc_coord

		if not self._pause:
			if direcao != self._ultima_direcao:
				if (direcao == Mover.FRENTE and self._ultima_direcao == Mover.TRAS) or \
					(direcao == Mover.TRAS and self._ultima_direcao == Mover.FRENTE) or \
					(direcao == Mover.DIREITA and self._ultima_direcao == Mover.ESQUERDA) or \
					(direcao == Mover.ESQUERDA and self._ultima_direcao == Mover.DIREITA):
					self._go_back()
				elif not (self._coord_x == 6 and self._coord_y == 6): 
					self._go_front()
				faixa_esq = self._gira2(direcao)
				self._encontra_faixa(faixa_esq)
				self._ultima_direcao = direcao
			else:
				self._go_front()
				self._encontra_faixa()

		# self.calibra_andando()
		# power, target, kp, kd, ki, direction, minref, maxref
		self._pause = False
		target = (self._min_ref + self._max_ref)/2
		self._anda(50, target, float(0.65), 1, float(0.02), 1, self._min_ref, self._max_ref)
		# self._anda_v1()
		self._finalizar_movimento()
		self._coord_x = calc_coord[0]
		self._coord_y = calc_coord[1]


	def stop(self, pause=False):
		"""Para os dois motores"""
		self.motor_esquerda.stop(stop_action='brake')
		self.motor_direita.stop(stop_action='brake')
		if pause:
			self._pause = True


	def _go_front(self):
		self.sensor_luminosidade.mode = 'COL-COLOR'
		cor = self.sensor_luminosidade.value()
		self.motor_esquerda.run_forever(speed_sp=100)
		self.motor_direita.run_forever(speed_sp=100)
		while True:
			if self.sensor_luminosidade.value() != cor:
				sleep(0.5)
				self.stop()
				break;

	def _go_back(self):
		self.sensor_luminosidade.mode = 'COL-COLOR'
		cor = self.sensor_luminosidade.value()
		self.motor_esquerda.run_forever(speed_sp=-100)
		self.motor_direita.run_forever(speed_sp=-100)
		while True:
			if self.sensor_luminosidade.value() != cor:
				sleep(0.5)
				self.stop()
				break;

	def _gira(self, angulo):
		"""Gira 90, -90, 180 ou 270 graus"""
		# TO_TEST: giro com sensor em modo de cor
		# self.sensor_luminosidade.mode = 'COL-COLOR'
		self.sensor_luminosidade.mode = 'COL-REFLECT'
		esquerda = False

		if angulo == 90:
			# gira pra direita
			self.motor_esquerda.run_forever(speed_sp=100)

		elif angulo == -90:
			# gira pra esquerda
			self.motor_direita.run_forever(speed_sp=100)
			self.motor_esquerda.run_forever(speed_sp=-100)
			esquerda = True

		elif abs(angulo) == 180:
			# gira 180
			for i in range(0, 2):
				self._gira(90)
			return

		elif angulo == -270:
			# gira pra direita
			self.motor_esquerda.run_forever(speed_sp=100)

		elif angulo == 270:
			# gira pra esquerda
			self.motor_direita.run_forever(speed_sp=50)
			self.motor_esquerda.run_forever(speed_sp=-150)
			esquerda = True

		sleep(0.2)
		while True:
			luminosidade = self.sensor_luminosidade.value()
			# if luminosidade != Cor.PRETO:
			# 	break

			if luminosidade <= (self._min_ref+5):
				if esquerda:
					esquerda = False
					sleep(0.5)
					continue
				sleep(0.4)
				self.stop()
				break;
			# TO_TEST:

		# while True:
		# 	luminosidade = self.sensor_luminosidade.value()
		# 	if luminosidade == Cor.PRETO:
		# 		sleep(0.4)
		# 		self.stop()
		# 		break
		
		# self.sensor_luminosidade.mode = 'COL-COLOR'
		# if self.sensor_luminosidade.value() == Cor.VERMELHO:


	def _gira2(self, direcao):
		"""Gira 90, -90, 180 ou 270 graus"""
		# TO_TEST: giro com sensor em modo de cor
		# self.sensor_luminosidade.mode = 'COL-COLOR'
		self.sensor_luminosidade.mode = 'COL-REFLECT'
		esquerda = False
		encontra_faixa_esquerda = False

		if direcao == self._ultima_direcao:
			return

		if direcao == Mover.FRENTE:
			if self._ultima_direcao == Mover.ESQUERDA:
				self.motor_esquerda.run_forever(speed_sp=100)
			elif self._ultima_direcao == Mover.DIREITA:
				# self.motor_direita.run_forever(speed_sp=25)
				self.motor_esquerda.run_forever(speed_sp=-100)
				encontra_faixa_esquerda  = True
			elif self._ultima_direcao == Mover.TRAS:
				self._gira2(Mover.ESQUERDA)
				return False

		elif direcao == Mover.DIREITA:
			if self._ultima_direcao == Mover.FRENTE:
				self.motor_esquerda.run_forever(speed_sp=100)
			elif self._ultima_direcao == Mover.TRAS:
				# self.motor_direita.run_forever(speed_sp=25)
				self.motor_esquerda.run_forever(speed_sp=-100)
				encontra_faixa_esquerda = True
			elif self._ultima_direcao == Mover.ESQUERDA:
				self._gira2(Mover.FRENTE)
				return False

		elif direcao == Mover.ESQUERDA:
			if self._ultima_direcao == Mover.FRENTE:
				# self.motor_direita.run_forever(speed_sp=25)
				self.motor_esquerda.run_forever(speed_sp=-100)
				encontra_faixa_esquerda = True
			elif self._ultima_direcao == Mover.TRAS:
				self.motor_esquerda.run_forever(speed_sp=100)
			elif self._ultima_direcao == Mover.DIREITA:
				self._gira2(Mover.TRAS)
				return False

		elif direcao == Mover.TRAS:
			if self._ultima_direcao == Mover.DIREITA:
				self.motor_esquerda.run_forever(speed_sp=100)
			elif self._ultima_direcao == Mover.ESQUERDA:
				# self.motor_direita.run_forever(speed_sp=25)
				self.motor_esquerda.run_forever(speed_sp=-100)
				encontra_faixa_esquerda = True
			elif self._ultima_direcao == Mover.FRENTE:
				self._gira2(Mover.DIREITA)
				return False

		else:
			return encontra_faixa_esquerda

		sleep(1)
		while True:
			luminosidade = self.sensor_luminosidade.value()
			# if luminosidade != Cor.PRETO:
			# 	break

			if luminosidade <= (self._min_ref+5):
				if esquerda:
					esquerda = False
					sleep(0.5)
					continue
				sleep(0.4)
				self.stop()
				break;
		return encontra_faixa_esquerda


	def _verifica_mutex(self):
		global movimento
		mutexMovimento.acquire()
		ret = movimento
		mutexMovimento.release()
		return ret


	def _steering(self, course, power):
		power_left = power_right = power
		s = (50 - abs(float(course))) / 50
		if course >= 0:
			power_right *= s
			if course > 100:
				power_right = - power
		else:
			power_left *= s
			if course < -100:
				power_left = - power
		return (int(power_left), int(power_right))

	def _anda(self, power, target, kp, kd, ki, direction, minRef, maxRef):
		lastError = error = integral = 0
		self.motor_esquerda.run_direct()
		self.motor_direita.run_direct()
		while True:
			mutex_val = self._verifica_mutex()
			if mutex_val == Mover.PARADO or mutex_val == Mover.EXIT:
				self.stop(True)
				break

			self.sensor_luminosidade.mode='COL-REFLECT'
			if self._next_coord == (6, 6):
				if int(lastError) < -30:
					self.stop()
					break

			# if (self.sensor_us.value()/10) < 10:
			# 	print("Obstaculo encontrado")
			# 	self.stop(True)
			# 	break

			refRead = self.sensor_luminosidade.value()
			error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
			derivative = error - lastError
			lastError = error
			integral = float(0.5) * integral + error
			course = (kp * error + kd * derivative +ki * integral) * direction
			for (motor, pow) in zip((self.motor_esquerda, self.motor_direita), self._steering(course, power)):
				motor.duty_cycle_sp = pow
			sleep(0.01) # Aprox 100Hz

			# Verifica cor
			self.sensor_luminosidade.mode='COL-COLOR'
			cor = self.sensor_luminosidade.value()
			if (cor != Cor.PRETO) and (cor != Cor.BRANCO):
				self.stop()
				break;


	def _anda_v1(self):
		speed = 360/4
		dt = 500
		stop_action = "brake"

		Kp = 1
		Ki = 0
		Kd = 0

		integral = 0
		previous_error = 0

		target_value = self.sensor_luminosidade.value()

		while True:
			distance = self.sensor_us.value() / 10

			error = target_value - self.sensor_luminosidade.value()
			integral += (error * dt)
			derivative = (error - previous_error) / dt

			u = (Kp * error) + (Ki * integral) + (Kd * derivative)

			if speed + abs(u) > 1000:
				if u >= 0:
					u = 1000 - speed
				else:
					u = speed - 1000

			if u >= 0:
				self.motor_esquerda.run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
				self.motor_direita.run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
				sleep(dt / 1000)
			else:
				self.motor_esquerda.run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
				self.motor_direita.run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
				sleep(dt / 1000)

			previous_error = error
			if error < -20:
				break
			# lum = self.sensor_luminosidade.value()
			# print("target: %d, lum: %d" % (target_value, lum))
			# if lum > (target_value + 10):
			# 	break

            # # Check if buttons pressed (for pause or stop)
            # if not self.btn.down:  # Stop
            #     print("Exit program... ")
            #     self.shut_down = True
            # elif not self.btn.left:  # Pause
            #     print("[Pause]")
            #     self.pause()

	def run(self):
		global movimento
		while True:
			mutexMovimento.acquire()
			move = movimento
			mutexMovimento.release()

			if move != Mover.PARADO:
				self.move(move)

			if move == Mover.EXIT:
				break

			sleep(1)


if __name__ == "__main__":
	mov = Mover(0, 0)
	mov.start()

	while True:
		cmd = input("Digite o comando: ")
		try:
			if str(cmd).lower() == 'w':
				if verifica_mutex_movimento() == 0:
					seta_mutex_movimento(Mover.FRENTE)
				else:
					print("Robo em movimento. Aguarde ...")
			elif str(cmd).lower() == 's':
				if verifica_mutex_movimento() ==  0:
					seta_mutex_movimento(Mover.TRAS)
				else:
					print("Robo em movimento. Aguarde ...")
			elif str(cmd).lower() == 'd':
				if verifica_mutex_movimento() ==  0:
					seta_mutex_movimento(Mover.DIREITA)
				else:
					print("Robo em movimento. Aguarde ...")
			elif str(cmd).lower() == 'a':
				if verifica_mutex_movimento() ==  0:
					seta_mutex_movimento(Mover.ESQUERDA)
				else:
					print("Robo em movimento. Aguarde ...")
			elif str(cmd).lower() == 'b':
				seta_mutex_movimento(Mover.PARADO)
			elif str(cmd).lower() == 'q':
				seta_mutex_movimento(Mover.EXIT)
				break
			else:
				print("Comando nao identificado.")

		except Exception as e:
			raise Exception(str(e))



