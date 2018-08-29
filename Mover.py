from ev3dev.ev3 import *
from time import time, sleep

class Mover(object):
	"""docstring for Mover"""
	FRENTE = 0
	TRAS = 1
	DIREITA = 2
	ESQUERDA = 3

	def __init__(self):
		self.status = 0
		self.motor_direita = Motor(OUTPUT_C)
		self.motor_esquerda = Motor(OUTPUT_B)
		self.sensor_us = UltrasonicSensor()
		self.sensor_luminosidade = ColorSensor()

		# assert cl.connected, "Connect a color sensor to any sensor port"
		self.sensor_luminosidade.mode = 'COL-REFLECT'
		self.sensor_us.mode = 'US-DIST-CM'

	def _encontra_linha(self):
		return

	def get_status(self):
		return self.status

	def move(self, direcao):


	def _gira(self, direcao):

	def _anda(self):
		speed = 360/4
		dt = 500
		stop_action = "coast"

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
			if previous_error < 0:
				break

            # # Check if buttons pressed (for pause or stop)
            # if not self.btn.down:  # Stop
            #     print("Exit program... ")
            #     self.shut_down = True
            # elif not self.btn.left:  # Pause
            #     print("[Pause]")
            #     self.pause()


if __name__ == "__main__":
	mov = Mover()
	# mov._calibra()
	# sleep(5)
	mov.move()
