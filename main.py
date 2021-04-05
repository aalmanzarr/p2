import os
import threading

from kernel.kernel import Kernel


if __name__ == "__main__":
    thread = None
    print("Verificando sistema")
    if not os.path.exists('./almacenamiento'):
        print("El sistema de archivos no existe")
        try:
            os.mkdir("./almacenamiento")
        except Exception as error:
            print(error)
            os._exit(os.EX_CANTCREAT)

        if os.path.exists("./almacenamiento"):
            print("Sistema de archivos creado")

    print("Siste de archivos chequeeado todo correcto")

    print("Iniciando....")
    kernel = Kernel()
    thread = threading.Thread(target=kernel.sistema)

    try:
        thread.start()
    except  Exception as error:
        print("Error iniciando")
        os._exit(os.EX_OSERR)

    
    