from ev3dev.ev3 import *
from time import time, sleep
from threading import Thread

class Mover(object):
	"""docstring for Mover"""
	FRENTE = 1
	DIREITA = 2
	TRAS = 3
	ESQUERDA = 4

	def __init__(self):
		self.status = 0
		self.motor_direita = Motor(OUTPUT_C)
		self.motor_esquerda = Motor(OUTPUT_B)
		self.sensor_us = UltrasonicSensor()
		self.sensor_luminosidade = ColorSensor()
		self.sensor_luminosidade.mode = 'COL-REFLECT'
		self.sensor_us.mode = 'US-DIST-CM'

		# assert cl.connected, "Connect a color sensor to any sensor port"

		# Atributos ocultos
		self._ultima_direcao = Mover.FRENTE
		self._min_ref = 5
		self._max_ref = 80
		self._firt_move = True


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
		self.motor_esquerda.run_direct(duty_cycle_sp=30)
		self.motor_direita.run_direct(duty_cycle_sp=30)
		self._max_ref = 0
		self._min_ref = 100
		end_time = time() + 5
		while time() < end_time:
			read = col.value()
			if self._max_ref < read:
				self._max_ref = read
			if self._min_ref > read:
				self._min_ref = read
		self.stop()


	def get_status(self):
		"""Retorna o status do robo:
			0 - parado
			1 - andando """
		return self.status


	def move(self, direcao):
		"""Move em uma direcao (frente, direita, esquerda, tras).
			Se for passada a mesma direcao, calibra e segue em fente"""
		if direcao != self._ultima_direcao:
			self._firt_move = False
			self._gira((direcao - self._ultima_direcao)*90)
			self._ultima_direcao = direcao
		elif not self._firt_move:
			# Calibra se a direcao for a mesma e nao for o primeiro movimento
			self.motor_direita.run_timed(time_sp=500, speed_sp=100)
			sleep(0.5)

		self.calibra_andando
		# power, target, kp, kd, ki, direction, minref, maxref
		target = (self._min_ref + self._max_ref)/2
		self._anda(50, target, float(0.65), 1, float(0.02), 1, self._min_ref, self._max_ref)
		# self._anda_v1()


	def stop(self):
		"""Para os dois motores"""
		self.motor_esquerda.stop(stop_action='brake')
		self.motor_direita.stop(stop_action='brake')


	def _gira(self, angulo):
		"""Gira 90, -90, 180 ou 270 graus"""
		direita = False
		if angulo == 90:
			# gira pra direita
			direta = True
			self.motor_esquerda.run_forever(speed_sp=100)

		elif angulo == -90:
			# gira pra esquerda
			self.motor_direita.run_forever(speed_sp=100)

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
			self.motor_direita.run_forever(speed_sp=100)

		while True:
			luminosidade = self.sensor_luminosidade.value()
			if luminosidade <= (self._min_ref+5):
				sleep(0.4)
				self.motor_esquerda.stop(stop_action='brake')
				self.motor_direita.stop(stop_action='brake')
				break;
		
		# if direita:
		# 	self.motor_direita.run_forever(speed_sp=100)
		# 	sleep(0.5)
		# 	self.motor_direita.stop(stop_action='brake')
		# else:
		# 	self.motor_esquerda.run_forever(speed_sp=100)
		# 	sleep(0.5)
		# 	self.motor_esquerda.stop(stop_action='brake')


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
			if int(lastError) < -20:
				self.stop()
				break

			if (self.sensor_us.value()/10) < 15:
				print("Obstaculo encontrado")
				self.stop()
				break

			refRead = self.sensor_luminosidade.value()
			error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
			derivative = error - lastError
			lastError = error
			integral = float(0.5) * integral + error
			course = (kp * error + kd * derivative +ki * integral) * direction
			for (motor, pow) in zip((self.motor_esquerda, self.motor_direita), self._steering(course, power)):
				motor.duty_cycle_sp = pow
			sleep(0.01) # Aprox 100Hz


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
			print(error)
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


if __name__ == "__main__":
	mov = Mover()

	while True:
		cmd = input("Digite o comando: ")
		try:
			if str(cmd).lower() == 'w':
				mov.move(Mover.FRENTE)
			elif str(cmd).lower() == 's':
				mov.move(Mover.TRAS)
			elif str(cmd).lower() == 'd':
				mov.move(Mover.DIREITA)
			elif str(cmd).lower() == 'a':
				mov.move(Mover.ESQUERDA)
			elif str(cmd).lower() == 'b':
				mov.stop()
			elif str(cmd).lower() == 'q':
				mov.stop()
				break
			else:
				print("Comando nao identificado.")

		except Exception as e:
			raise Exception('ERRO: %s' % str(e))



