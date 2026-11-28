
import numpy
from .agent import Road, Traffic_Light, Destination

#vector de movimiento de cada dirección del mapa 
DIRECCIONES = {
    "Right": (1, 0),
    "Left": (-1, 0),
    "Up": (0, 1),
    "Down": (0, -1),
}

#dirección opuesta de cada dirección
OPUESTA = {"Right": "Left", "Left": "Right", "Up": "Down", "Down": "Up"}

#& convierte una coordenada (x, y) en el número de celda que se usa en la matriz S
#in: la coordenada y el tamaño del mapa (ancho, alto)
#out: el número de la celda
def numeroCelda(coord, forma):
    return int(numpy.ravel_multi_index(coord, forma))

#& convierte un número de celda de la matriz S de regreso a su coordenada (x, y)
#in: el número de la celda y el tamaño del mapa (ancho, alto)
#out: la coordenada de la celda
def coordCelda(numero, forma):
    x, y = numpy.unravel_index(numero, forma)
    return (int(x), int(y))

#& suma una dirección a una coordenada
#in: una coordenada y una dirección
#out: la coordenada de la celda vecina en esa dirección
def mover(coord, direccion):
    dx, dy = DIRECCIONES[direccion]
    return (coord[0] + dx, coord[1] + dy)

#& regresa la dirección de una celda por la que se puede circular
#in: el agente fijo de una celda
#out: su dirección, o nada si no es calle ni semáforo
def direccionCelda(agente):
    if isinstance(agente, (Road, Traffic_Light)):
        return agente.direction
    return None

#& deduce la dirección de un semáforo a partir de las calles
#in: el mapa estático y la coordenada del semáforo
#out: la dirección que controla el semáforo, o nada si no se pudo deducir
def inferirDireccionSemaforo(mapaEstatico, coord):
    #! apoyo de ia: ¿cómo sabe la direccion de los semaforos?
    # el mapa no trae la dirección del semáforo, así que se "vota" con las calles vecinas:
    #una calle cuenta si está en la misma línea que su dirección, es decir,
    #si apunta hacia el semáforo (está detrás) o si el semáforo desemboca en ella (está adelante)
    votos = {}
    for direccion in DIRECCIONES:
        atras = mapaEstatico.get(mover(coord, OPUESTA[direccion]))
        adelante = mapaEstatico.get(mover(coord, direccion))
        for vecino in (atras, adelante):
            if isinstance(vecino, Road) and vecino.direction == direccion:
                votos[direccion] = votos.get(direccion, 0) + 1

    if not votos:
        return None
    #gana la dirección con más votos
    return max(votos, key=votos.get)

#& revisa si en un fin de calle se puede girar hacia un lado
#in: el mapa estático, la celda donde se acaba la calle, su dirección y el lado hacia el que se quiere girar
#out: verdadero si hacia ese lado hay una calle que va en esa misma dirección
def giroPermitido(mapaEstatico, coord, direccion, lado):
    #se brincan los carriles paralelos al nuestro (misma dirección) hasta topar
    #con la calle transversal; se puede girar solo si esa calle va hacia el lado del giro.
    #así dos carriles paralelos que terminan juntos no giran uno hacia el otro (evita ciclos)
    actual = mover(coord, lado)
    while direccionCelda(mapaEstatico.get(actual)) == direccion:
        actual = mover(actual, lado)
    return direccionCelda(mapaEstatico.get(actual)) == lado

#& aplica las reglas de las calles para saber a qué celdas se puede mover un coche desde una celda
#in: el mapa estático y la coordenada de la celda
#out: la lista de coordenadas a las que se puede mover en un step
def movimientosPermitidos(mapaEstatico, coord):
    direccion = direccionCelda(mapaEstatico.get(coord))
    if direccion is None:
        #de obstáculos y destinos no se sale: un destino es final,
        #así ningún coche usa el destino de otro como atajo
        return []

    movimientos = []

    #regla 1: seguir de frente
    #se avanza a la celda de enfrente para que no vaya en sentido contrario
    frente = mover(coord, direccion)
    agenteFrente = mapaEstatico.get(frente)
    direccionFrente = direccionCelda(agenteFrente)
    if direccionFrente is not None and direccionFrente != OPUESTA[direccion]:
        movimientos.append(frente)
    elif isinstance(agenteFrente, Destination):
        movimientos.append(frente)

    #la calle termina si enfrente hay un edificio o el borde del mapa
    finDeCalle = direccionFrente is None and not isinstance(agenteFrente, Destination)

    #los lados de una calle horizontal son arriba y abajo; los de una vertical, izquierda y derecha
    if direccion in ("Right", "Left"):
        lados = ("Up", "Down")
    else:
        lados = ("Left", "Right")

    for lado in lados:
        lateral = mover(coord, lado)
        agenteLateral = mapaEstatico.get(lateral)
        direccionLateral = direccionCelda(agenteLateral)

        #regla 2: incorporarse a una calle de un lado solo si fluye en el mismo sentido (cruces)
        if direccionLateral == lado:
            movimientos.append(lateral)
        # se permite girar hacia el lado si llegamos al fin del mapa
        elif finDeCalle and giroPermitido(mapaEstatico, coord, direccion, lado):
            movimientos.append(lateral)
        elif isinstance(agenteLateral, Destination):
            #también se entra de lado a un destino que está junto a la calle
            movimientos.append(lateral)

        #regla 3: cambio de carril en diagonal hacia adelante solo si es la misma dirección, y debe ser calle
        diagonal = mover(frente, lado)
        if direccionCelda(mapaEstatico.get(diagonal)) == direccion and direccionLateral is not None:
            movimientos.append(diagonal)

    return movimientos

#& arma la matriz de estados S: para cada celda, a qué celdas se puede mover un coche
#in: el mapa estático y el tamaño del mapa (ancho, alto)
#out: una matriz donde S[a, b] = 1 si un coche puede ir de la celda a a la celda b en un step
def matrizEstados(mapaEstatico, forma):
    totalCeldas = forma[0] * forma[1]
    estados = numpy.zeros((totalCeldas, totalCeldas), dtype=numpy.int8) #por espacio porque solo son 0 y 1
    for coord in mapaEstatico:
        origen = numeroCelda(coord, forma)
        for destino in movimientosPermitidos(mapaEstatico, coord):
            estados[origen, numeroCelda(destino, forma)] = 1
    return estados

#& celdas a las que se puede mover un coche desde una celda (el renglón de S)
#in: la matriz S y el número de la celda
#out: los números de las celdas a las que se puede ir
def sucesores(estados, celda):
    return [int(c) for c in numpy.where(estados[celda, :] != 0)[0]]

#& celdas desde las que un coche puede llegar a una celda (la columna de S)
#in: la matriz S y el número de la celda
#out: los números de las celdas desde las que se llega a ella
def predecesores(estados, celda):
    #como las calles son de un solo sentido, no es lo mismo que los sucesores;
    #d* lite los ocupa porque busca desde el destino hacia el coche
    return [int(c) for c in numpy.where(estados[:, celda] != 0)[0]]

#& busca en anchura (BFS) todas las celdas a las que se puede llegar desde una celda
#in: la matriz S y la celda de inicio
#out: el conjunto de celdas alcanzables, incluyendo la de inicio
def celdasAlcanzables(estados, inicio):
    alcanzables = {inicio}
    cola = [inicio]
    indice = 0
    while indice < len(cola):
        actual = cola[indice]
        indice += 1
        for vecino in sucesores(estados, actual):
            if vecino not in alcanzables:
                alcanzables.add(vecino)
                cola.append(vecino)
    return alcanzables

#& busca en anchura (BFS) hacia atrás todas las celdas desde las que se llega a alguno de los destinos
#in: la matriz S y las celdas destino
#out: el conjunto de celdas que tienen camino a algún destino, incluyendo los destinos
def celdasQueLleganADestino(estados, destinos):
    #es la misma BFS pero usando predecesores (columnas de S) en lugar de sucesores
    llegan = set(destinos)
    cola = list(destinos)
    indice = 0
    while indice < len(cola):
        actual = cola[indice]
        indice += 1
        for vecino in predecesores(estados, actual):
            if vecino not in llegan:
                llegan.add(vecino)
                cola.append(vecino)
    return llegan

#& valida que desde cada punto de inicio se pueda llegar a cada destino
#in: la matriz S, las celdas de inicio y las celdas destino
#out: los pares (inicio, destino) que no tienen camino; vacía si todo está bien
def validarGrafo(estados, inicios, destinos):
    faltantes = []
    for inicio in inicios:
        alcanzables = celdasAlcanzables(estados, inicio)
        for destino in destinos:
            if destino not in alcanzables:
                faltantes.append((inicio, destino))
    return faltantes

#& busca callejones sin salida: celdas por las que se circula pero desde las que no se llega a ningún destino
#in: la matriz S y las celdas destino
#out: los números de las celdas sin camino a un destino
def buscarCallejones(estados, destinos):
    llegan = celdasQueLleganADestino(estados, destinos)
    #solo cuentan las celdas por las que se circula (las que tienen algún 1 en su renglón)
    circulables = [int(c) for c in numpy.where(estados.sum(axis=1) > 0)[0]]
    return [c for c in circulables if c not in llegan]
