import threading  #Hilos
import time       #Pausas

class Filosofo(threading.Thread):
    def __init__(self, i, izquierda, derecha, camarero, estados): #Establecer los parametros de la clase FIloso para cada uno de estos
        threading.Thread.__init__(self)
        self.index = i #Hace referencia al filosofo
        #palillos
        self.izquierda = izquierda
        self.derecha = derecha
        #palillos
        self.camarero = camarero
        self.estados = estados #varian entre pensando y comiendo
        self.cambios = 1 #contador de cambion NO NECESARIO

    def run(self):
       # while True: #Para Ejecucion continua sin limite de repeticiones
        while self.cambios < 10:  # Ejecutar hasta que se realicen 10 cambios de estado NO NECESARIO
            #self.cambios se utiliza para aumentar el contador de cambios de los filosos NO NECESARIO
            self.estados[self.index] = "pensando"
            self.cambios +=1
            time.sleep(1) 
            #Acquire utlizado para que el camarero tome propiedad del objeto palillos
            self.camarero.acquire()  # El camarero limita la cantidad de filósofos que pueden tomar palillos
            self.izquierda.acquire()
            self.derecha.acquire()
            #Cambio de estado del filoso a Comiendo
            self.estados[self.index] = f"I{self.index} comiendo D{self.index}"
            self.cambios += 1
            time.sleep(1) 
            #Release se ha utilizado para que el filoso suelte los palillos
            self.derecha.release()
            self.izquierda.release()
            self.camarero.release()

# Crear los palillos (semáforos)
palillos = [threading.Semaphore(1) for _ in range(5)]

# Crear el camarero (semáforo)
camarero = threading.Semaphore(4)  # Permite que se tomen 4 palillos
print("Nombres de los filosofos: [Socrates  ,  Platon   ,   Tales   , Heraclito , Aristoteles]") #NO ES NECESARIO solo ilustrativo
# Crear la lista de estados de los filósofos
estados = ["pensando"] * 5

# Crear los filósofos
filosofos = []
for i in range(5):
    izquierda = palillos[i]
    derecha = palillos[(i + 1) % 5]
    filosofo = Filosofo(i, izquierda, derecha, camarero, estados) #Crea objetos clase Filosofos
    filosofos.append(filosofo)
    filosofo.start() #Inicia el metodo Run


#while True:

while any(filosofo.cambios < 10 for filosofo in filosofos):
    print("Estados de los filósofos:", estados)# Impresion de estados formato : F0,F1,F2,F3
    time.sleep(1)
    print() 
print("Los filósofos han acabado la comida del restaurante")
