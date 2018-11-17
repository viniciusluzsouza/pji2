from transmissor_sr import *
from receptor_sr import *
from transmissor_sa import *
from receptor_sa import *
from gerenciador import *
from time import sleep

def main():
	gerente = Gerenciador()

	transmissorsr = TransmissorSR("localhost")
	transmissorsr.start()

	receptorsr = ReceptorSR("localhost")
	receptorsr.start()

	transmissorsa = TransmissorSA("localhost")
	transmissorsa.start()

	receptorsa = ReceptorSA("localhost")
	receptorsa.start()

	gerente.start()

if __name__ == '__main__':
	main()