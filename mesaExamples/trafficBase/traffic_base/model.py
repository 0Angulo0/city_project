from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from .agent import *
from .graph import matrizEstados, inferirDireccionSemaforo
import json

# mapa que se usa en la simulación
MAP_FILE = "city_files/2025_base.txt"


class CityModel(Model):

    #& crea el modelo de la ciudad a partir del mapa y construye el grafo de calles
    #in: número de agentes, semilla aleatoria
    #out: nada 
    def __init__(self, N, seed=42):

        super().__init__(seed=seed)

        #el diccionario traduce cada carácter del mapa al agente que le corresponde
        with open("city_files/mapDictionary.json") as dictFile:
            dataDictionary = json.load(dictFile)

        self.num_agents = N
        self.traffic_lights = []
        self.destinations = []

        #mapa estático, lo usa el grafo para saber qué hay en cada celda
        self.static_map = {}

        #cada carácter del archivo de mapa representa un agente
        with open(MAP_FILE) as baseFile:
            # splitlines separa las filas sin dejarles el \n al final
            lines = baseFile.read().splitlines()
            self.width = len(lines[0])
            self.height = len(lines)

            self.grid = OrthogonalMooreGrid(
                [self.width, self.height], capacity=100, torus=False, random=self.random
            )

            #recorre cada carácter del mapa y crea el agente correspondiente
            for r, row in enumerate(lines):
                for c, col in enumerate(row):

                    #la fila 0 del archivo es la de arriba, pero en mesa crece hacia arriba
                    coord = (c, self.height - r - 1)
                    cell = self.grid[coord]

                    if col in ["v", "^", ">", "<"]:
                        agent = Road(self, cell, dataDictionary[col])

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(
                            self,
                            cell,
                            False if col == "S" else True,
                            int(dataDictionary[col]),
                        )
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(self, cell)

                    elif col == "D":
                        agent = Destination(self, cell)
                        self.destinations.append(agent)

                    self.static_map[coord] = agent

        #! el mapa no trae la dirección de los semáforos, se deduce de sus calles vecinas
        for light in self.traffic_lights:
            light.direction = inferirDireccionSemaforo(self.static_map, light.cell.coordinate)

        #los puntos de inicio son las 4 esquinas del mapa 
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        self.start_cells = [
            self.grid[coord] for coord in corners
            if isinstance(self.static_map.get(coord), (Road, Traffic_Light))
        ]

        #matriz de estados S
        self.estados = matrizEstados(self.static_map, (self.width, self.height))

        self.running = True

    #& avanza el modelo un step
    def step(self):
        self.agents.shuffle_do("step")
