import threading
import time

class Filosofo(threading.Thread):
    def __init__(self, i, izquierda, derecha, camarero, estados):
        threading.Thread.__init__(self)
        self.index = i
        self.izquierda = izquierda
        self.derecha = derecha
        self.camarero = camarero
        self.estados = estados

    def run(self):
        while True:
            # Filósofo piensa
            self.estados[self.index] = "pensando"
            time.sleep(1)  # Esperar un segundo

            self.camarero.acquire()  # El camarero limita la cantidad de filósofos que pueden tomar palillos

            self.izquierda.acquire()
            self.derecha.acquire()

            # Filósofo come
            self.estados[self.index] = "comiendo"
            time.sleep(1)  # Esperar un segundo

            self.derecha.release()
            self.izquierda.release()

            self.camarero.release()

# Crear los palillos (semáforos)
palillos = [threading.Semaphore(1) for _ in range(5)]

# Crear el camarero (semáforo)
camarero = threading.Semaphore(4)  # Permite que cuatro filósofos tomen palillos al mismo tiempo

# Crear la lista de estados de los filósofos
estados = ["pensando"] * 5

# Crear los filósofos
filosofos = []
for i in range(5):
    izquierda = palillos[i]
    derecha = palillos[(i + 1) % 5]
    filosofo = Filosofo(i, izquierda, derecha, camarero, estados)
    filosofos.append(filosofo)
    filosofo.start()

# Monitorear los estados de los filósofos
while True:
    time.sleep(1)  # Esperar un segundo
    print("Estados de los filósofos:", estados)
