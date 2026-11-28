from mesa.discrete_space import CellAgent
from .agent import Traffic_Light
from .graph import numeroCelda, coordCelda, direccionCelda
from .dstar_lite import DStarLite

class Car(CellAgent):

    #& crea un coche y le calcula su primer camino hacia el destino
    #in: el modelo, la celda donde aparece y el destino al que tiene que llegar, out: nada
    def __init__(self, model, cell, destino):
        super().__init__(model)
        self.cell = cell
        self.destino = destino
        self.forma = (model.width, model.height)

        inicio = numeroCelda(cell.coordinate, self.forma)
        meta = numeroCelda(destino.cell.coordinate, self.forma)
        self.ruta = DStarLite(model.estados, self.forma, inicio, meta)

        #estado: "moving", "waiting_car" o "waiting_light"
        self.estado = "moving"
        #cara del coche para saber cual es el frente
        self.direccion = direccionCelda(model.static_map.get(cell.coordinate))
        #steps seguidos que lleva esperando por otros coches
        self.pasosEsperando = 0
        #celdas a las que se les puso costo extra en el último recálculo
        self.celdasConTrafico = []

    #& decide y hace cada acción
    def step(self):
        #capa 1: llegar. si ya está en su destino, sale de la simulación
        if self.cell == self.destino.cell:
            self.model.cochesLlegaron += 1
            self.remove()
            return

        siguiente = self.siguienteCelda()

        #capa 2: evitar congestión; si lleva mucho atorado por coches, busca otra ruta.
        if self.pasosEsperando >= 3: #3 es su "paciencia"
            self.evitarTrafico()
            siguiente = self.siguienteCelda()

        #capa 3: no chocar; si hay un coche en la siguiente celda, espera
        if any(isinstance(agente, Car) for agente in siguiente.agents):
            self.estado = "waiting_car"
            #para buscar otra ruta solo cuenta la espera por coches, no la de los semáforos
            self.pasosEsperando += 1
            return

        #capa 4: respetar el semáforo; state es verdadero cuando está en verde
        agente = self.model.static_map.get(siguiente.coordinate)
        if isinstance(agente, Traffic_Light) and not agente.state:
            self.estado = "waiting_light"
            return

        #capa 5: seguir la ruta
        nuevaDireccion = direccionCelda(agente)
        if nuevaDireccion is not None:
            self.direccion = nuevaDireccion

        self.cell = siguiente
        self.ruta.moverInicio(numeroCelda(siguiente.coordinate, self.forma))
        self.estado = "moving"
        self.pasosEsperando = 0

    #& pregunta a d* lite cuál es la siguiente celda del camino
    #in: nada. out: la celda de mesa a la que se debe mover el coche
    def siguienteCelda(self):
        numero = self.ruta.siguienteCelda()
        return self.model.grid[coordCelda(numero, self.forma)]

    #& sube el costo de las celdas con coches que ve el coche y le pide a d* lite que repare la ruta
    def evitarTrafico(self):
        nuevas = []
        for celda in self.cell.get_neighborhood(radius=2): #que tan lejos ve un coche 
            if any(isinstance(agente, Car) for agente in celda.agents):
                nuevas.append(numeroCelda(celda.coordinate, self.forma))

        #las celdas del recálculo anterior regresan a su costo normal
        #y las que tienen coche ahorita se vuelven más caras (si se repite una, gana el costo nuevo)
        cambios = {}
        for celda in self.celdasConTrafico:
            cambios[celda] = 0
        for celda in nuevas:
            #aquí se cambia el costo extra de pasar por una celda con coche
            cambios[celda] = 5

        self.ruta.cambiarCostos(cambios)
        self.celdasConTrafico = nuevas
        self.pasosEsperando = 0
