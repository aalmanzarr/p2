import time
import random

from multiprocessing.dummy.connection import Connection
from sistema import Sistema

class Main(Sistema):
    def rand_mult(self,pipe: Connection):
        while self.running:
            rand=random.randint(0,1000)
            rand2=random.randint(0,1000) 
            pipe.send({
                    "cmd": "send",
                    "src": "application/app3",
                    "dst": "archivos",
                    "msg" : f"log |Numeros generados {rand} y {rand2}, su multiplicación es: {rand+rand2} "
                })
            if rand % 2 == 0 or rand2 % 2 == 0:
                self.running = False
                pipe.send({
                    "codterm": 2,
                    "msg": "Error"
                })

            if rand * rand2 > 75000:
                raise Exception("Out Exception")

            time.sleep(5)