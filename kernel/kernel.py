import threading
import time

from multiprocessing import Pipe
from multiprocessing.dummy.connection import Connection
from aplicaciones.aplicaciones import Aplicaciones
from GUI.GUI import GUI
from archivos.archivos import Archivos


class Kernel:
    __GUI_hilo = None
    __archivos_hilo = None
    __aplicacion_hilo = None
    __pipe_GUI, __pipe_GUI2 = None, None
    __pipe_archivos, __pipe_archivos2 = None, None
    __pipe_aplicaciones, __pipe_aplicaciones2 = None, None
    _kernel = True

    def sistema(self):
        self.__pipe_GUI, self.__pipe_GUI2 = Pipe()
        self.__pipe_aplicaciones, self.__pipe_aplicaciones2 = Pipe()
        self.__pipe_archivos, self.__pipe_archivos2 = Pipe()

        gui = GUI(self.__pipe_GUI2)
        archivos = Archivos(self.__pipe_archivos2)
        aplicaciones = Aplicaciones(self.__pipe_aplicaciones2)

        self.__GUI_hilo = threading.Thread(target=gui.escuchar)
        self.__archivos_hilo = threading.Thread(target=archivos.escuchar)
        self.__aplicacion_hilo = threading.Thread(target=aplicaciones.escuchar)

        self.__archivos_hilo.start()
        self.__aplicacion_hilo.start()
        self.__GUI_hilo.start()

        self.sistema_interno()

    def escuchar_pipes(self, conexion: Connection):
        while True:
            if not conexion.poll(3):
                time.sleep(0.2)
                continue

            message = conexion.recv()

            if 'cmd' in message:
                if message['cmd'] == "send":
                    pass
                elif message['cmd'] == "info":
                    pass
                elif message['cmd'] == "stop":
                    pass

            elif 'codterm' in message:
                if message['codterm'] == 0:
                    print("Operación exitosa")
                elif message['codterm'] == 1:
                    print("Modulo ocupado")
                elif message['codterm'] == 2:
                    print("")

    def encontrar_destino(self, message, action=None):
        if message['dst'] == "archivos":
            self.__pipe_archivos.send(message['msg'])
        elif message['dst'] == "GUI":
            self.__pipe_GUI.send(message['msg'])
        elif message['dst'] == "aplicaciones":
            self.__pipe_aplicaciones.send(message['msg'])
        elif message['dst'] == "kernel":
            if action == "stop":
                self.terminar(message['src'])

            if not action:
                if message['msg'] == "sysinfo":
                    self.__pipe_GUI.send({
                        "cmd": 'info',
                        "src": "kernel",
                        "dst": 'GUI',
                        "msg": {
                            "GUI": self.__GUI_hilo.is_alive(),
                            "files_manager": self.__archivos_hilo.is_alive(),
                            "applications": self.__aplicacion_hilo.is_alive(),
                            "kernel": self._kernel_status
                        }

                    }) 

        else:
            print("Destino no encontrado")

    def terminar(self, instancia):
        if instancia == "GUI":
            self.__GUI_hilo._stop()
            self.__GUI_hilo.join()
        elif instancia == "aplicaciones":
            self.__aplicacion_hilo._stop()
            self.__aplicacion_hilo.join()
        elif instancia == "archivos":
            self.__archivos_hilo._stop()
            self.__archivos_hilo.join()

    def sistema_interno(self):
        mensajes_gui = threading.Thread(target=self.escuchar_pipes, args=[self.__pipe_GUI])
        mensajes_archivos = threading.Thread(target=self.escuchar_pipes, args=[self.__pipe_archivos])
        mensajes_aplicacion = threading.Thread(target=self.escuchar_pipes, args=[self.__pipe_aplicaciones])

        mensajes_gui.start()
        mensajes_archivos.start()
        mensajes_aplicacion.start()

        while self._kernel:
            time.sleep(0.2)

        mensajes_gui._stop()
        mensajes_archivos._stop()
        mensajes_aplicacion._stop()
