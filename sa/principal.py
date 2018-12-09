from gerenciador import *
from status import *

status = Status()

gerenciador = Gerenciador(status)
gerenciador.init_thread_rede()
