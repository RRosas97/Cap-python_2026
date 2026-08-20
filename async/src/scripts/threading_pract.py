import threading
import time


def desayunar():
    print("Iniciando desayuno...")
    time.sleep(3)
    print("Terminando desayuno...")


def tomar_cafe():
    print("Iniciando cafe...")
    time.sleep(4)
    print("Terminando cafe...")


def estudiar():
    print("Iniciando estudiar...")
    time.sleep(5)
    print("Terminando estudiar...")


inicio = time.perf_counter()
desayuno = threading.Thread(target=desayunar, args=())
desayuno.start()
cafe = threading.Thread(target=tomar_cafe, args=())
cafe.start()
estudio = threading.Thread(target=estudiar, args=())
estudio.start()
# desayunar()
# tomar_cafe()
# estudiar()

# print(threading.active_count())
# print(threading.enumerate())

desayuno.join()
cafe.join()
estudio.join()

fin = time.perf_counter()

tiempo_secuencial = fin - inicio
print(tiempo_secuencial)
