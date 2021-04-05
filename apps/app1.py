import time
import random

from multiprocessing.dummy.connection import Connection
from sistema import Sistema

class Main(Sistema):
    def rand_sum(self,pipe: Connection):
        while self.running:
            rand=random.randint(0,1000)
            rand2=random.randint(0,1000) 

            pipe.send({
                "cmd": "send",
                "src": "application/app1",
                "dst": "archivos",
                "msg" : f"log |Numeros generados {rand} y {rand2}, su suma es: {rand+rand2} "
            })
            

            if rand + rand2 > 1500:
                self.running = False
                pipe.send({
                    "codterm": 2,
                    "msg": "Error"
                })

            if sum %5 ==0:
                raise Exception("Out Exception")

            time.sleep(5)