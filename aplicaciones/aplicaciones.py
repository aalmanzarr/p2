import time

from multiprocessing.dummy.connection import Connection
from apps.app1 import Main as suma
from apps.app2 import Main as nota
from apps.app3 import Main as multiplicacion

class Aplicaciones:
    __pipe: Connection = None
    __hilo = None
    aplicaciones = []

    def __init__(self, pipe):
        self.__pipe = pipe

    def escuchar(self):
        print("INiciando aplicaciones")
        while True:
            if not self.__pipe.poll(3):
                time.sleep(0.2)
                continue

            mensaje = self.__pipe.recv()
            mensaje = mensaje.split("|")

            if len(mensaje) == 0 and mensaje[0] == "halt":
                self.__pipe.send({
                    "cmd": "stop",
                    "src": "applications",
                    "dst": "kernel",
                    "msg": "Stopped by user"
                })
                self.parar_apps()
            else:
                if mensaje[0] == "lanzar":
                    pass
                if mensaje[0] == "listar":
                    self.listar_apps()
                if mensaje[0] == "parar":
                    self.parar_apps(mensaje[1])

    def listar_apps(self):
        apps = [f"{app['pid']} - {app['hilo'].getName()}" for app in self.aplicaciones]
        self.__pipe.send({
            "cmd": "info",
            "src": "applications",
            "dst": "GUI",
            "msg": apps
        })

    def parar_apps(self, app=None):
        if app:
            _app = next((__app for __app in self.aplicaciones if __app['pid'] == int(app)), None)

            _app['app'].stop()
            _app['hilo'].join()

            self.aplicaciones.remove(_app)
        else:
            for _app in reversed(self.aplicaciones):
                _app['app'].stop()
                _app['hilo'].join()
                self.aplicaciones.remove(_app)

    def launch_app(self, app_name):
        pass