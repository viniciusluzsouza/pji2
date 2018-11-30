from threading import Lock, Event


def init():
    global solicita_gerente, gerente_msg_lock, gerente_msg, transmitir_event, transmitir_msg_lock, transmitir_msg
    global transmitir_toUI_event, transmitir_toUI_lock, transmitir_toUI

    solicita_gerente = Event()
    gerente_msg_lock = Lock()
    gerente_msg = {}

    transmitir_event = Event()
    transmitir_msg_lock = Lock()
    transmitir_msg = {}

    transmitir_toUI_event = Event()
    transmitir_toUI_lock = Lock()
    transmitir_toUI = {}