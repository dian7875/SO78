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
        self.cambios = 0  # Contador de cambios de estado

    def run(self):
        while self.cambios < 10:  # Ejecutar hasta que se realicen 10 cambios de estado
            # Filósofo piensa
            self.estados[self.index] = "pensando"
            time.sleep(1)  # Esperar un segundo

            self.camarero.acquire()  # El camarero limita la cantidad de filósofos que pueden tomar palillos

            self.izquierda.acquire()
            self.derecha.acquire()

            # Filósofo come
            self.estados[self.index] = f"I{self.index} comiendo D{self.index}"
            self.cambios += 1  # Incrementar el contador de cambios de estado
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

# Monitorear los cambios de estado
while any(filosofo.cambios < 10 for filosofo in filosofos):
    print("Estados de los filósofos:", estados)
    time.sleep(1)  # Esperar un segundo antes de imprimir los estados nuevamente
    print()  # Salto de línea

print("Los filósofos han acabado la comida del restaurante")
