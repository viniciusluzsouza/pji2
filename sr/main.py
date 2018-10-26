from transmissor import *
from receptor import *
from interface import *

if __name__ == "__main__":
	t = Transmissor("localhost")
	t.start()

	r = Receptor("localhost")
	r.start()

	i = InterfaceSR()
	i.start()

	# for cmd in range (1000, 1004):
	# 	print("ENTER PARA ENVIAR MENSAGEM AO SS")
	# 	input()

	# 	msg = {'cmd': cmd}
	# 	shared_obj.set(SharedObj.TransmitirLock, msg)
	# 	shared_obj.set_event(SharedObj.TransmitirEvent)

	# 	sleep(2)

