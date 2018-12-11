from gerenciador import *
from status import *
from Interface import *
status = Status()

gerenciador = Gerenciador(status)
gerenciador.init_thread_rede()

#ui = target=InterfaceGrafica(status)
#ui.start()

