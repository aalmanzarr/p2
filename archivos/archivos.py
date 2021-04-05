import time
import logging
import os

from multiprocessing.dummy.connection import Connection


class Archivos:
    __pipe: Connection = None
    __hilo = None

    def __init__(self, pipe):
        self.__pipe = pipe

    def escuchar(self):
        manejador = logging.FileHandler('./almacenamiento/logs', 'a')

        log = logging.getLogger()
        for hdlr in log.handlers[:]:
            log.removeHandler(hdlr)

        log.addHandler(manejador)

        while True:
            if not self.__pipe.poll(3):
                time.sleep(0.2)
                continue

            mensaje = self.__pipe.recv()
            mensaje = mensaje.split('|')

            if mensaje[0].lower() == 'log':
                logging.info(mensaje[1])

            if mensaje[0].lower() == 'read':
                with open('./almacenamiento/logs', "r") as logs:
                    lines = logs.readlines()
                    last_lines = lines[-5:]
                    self.__pipe.send({
                        "cmd": "info",
                        "src": "GestorArc",
                        "dst": "GUI",
                        "msg": last_lines
                    })
            if mensaje[0].lower() == 'folder':
                self.manejar_folders(int(mensaje[1]), mensaje[2])

    def manejar_folders(self, operation, name):
        if operation == 0:
            os.mkdir(f'./almacenamiento/{name}')
        if operation == 1:
            os.rmdir(f'./almacenamiento/{name}')