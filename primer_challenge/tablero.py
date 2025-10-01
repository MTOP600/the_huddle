import heapq
import numpy as np


def heuristica(inicio, fin):

    #desempaquetamos las coordenadas correspondientes
    inicio_x, inicio_y = inicio
    fin_x, fin_y = fin

    # Distancia Manhattan
    return abs(inicio_x - fin_x) + abs(inicio_y - fin_y)

#creamos una funcion a la que se le pasa la coordenada de una celda y en base a eso me devuelve una lista de direcciones a las que me puedo mover
def celdas_transitables(tablero, celda_actual):

    #desempaquetamos la coordenada de la celda actual
    actual_x, actual_y = celda_actual

    #creamos una lista de las direcciones a las que nos podremos mover
    direcciones_disponibles = []

    #tupla de direcciones a las que probaremos movernos
    movimientos = [(0,1), (1,0), (0,-1), (-1,0)]

    # .shape nos devuelve el tamano del arreglo en cada dimension, de ahi tomamos filas y columnas
    filas, columnas = tablero.shape

    #iteramos en las posibles direcciones para movernos
    for dx, dy in movimientos:

        #sumamos el posible movimiento a las coordenadas actuales para simular un paso
        posible_x = actual_x + dx
        posible_y = actual_y + dy

        # nos aseguramos que la posicion no se salga del tablero
        if 0 <= posible_x < columnas and 0 <= posible_y < filas:

            #hallamos el peso de la celda (el peso indica que tipo de terreno es)
            peso = tablero[posible_y, posible_x]

            #si el peso es 9, el terreno es infranqueabe, lo que significa que no nos podemos mover por ahi
            if peso != 9:  # 9 = montaña, no transitable

                #si la posicion es totalmente valida, la agregamos a la lista de posiciones a las que nos podemos mover
                direcciones_disponibles.append((posible_x, posible_y))

    # cuando tengamos todas las posiciones posibles a las que movernos retornasmos la lista
    return direcciones_disponibles

#este es la funcion que hace de cerebro para el programa y que pueda hallar un camino
def a_estrella(inicio, fin, tablero):

    #hacemos una cola para probar las direcciones
    cola_prioridad = []

    #esto es un monticulo, lo que estamos haciendo es organizar la cola_prioridad en base a el numero heuristica, lo que hace es ordenar
    #la lisra cola_prioridad de menor a mayor, haciendonos mas facil tomar la decision de hacia donde movernos (heuristica mas pequena,
    #movimiento mas conveniente), el elemento con menor valor de  heuristica esta siempre en la raiz de la cola
    heapq.heappush(cola_prioridad, (heuristica_inicio, inicio))

    #diccionario con lo que nos cuesta movernos hasta x celda
    diccionario_costos = {inicio: 0}

    #usamos esto para luego volver sobre nuestros pasos y hallar el camino
    diccionario_padres = {}

    #inicializamos un set de visitados para no quedar en bucles infinitos
    visitados = set()

    #la heuristica sirve como una brujula que nos dice mas o menos hacia donde debemos probar
    heuristica_inicio = heuristica(inicio, fin)


    #hacemos un while que se ejecuta siempre que haya lugares a los que movernos
    while cola_prioridad:

        #obetenemos el primer elemento (heuristica mas pequena) de la tupla cola_prioridad, ignoramos el valor de la heuristica con _ ya que no lo vamos a usar
        #aqui, solamente nos interesa celda actual
        _, celda_actual = heapq.heappop(cola_prioridad)

        #si llegamos al fin, salimos del while
        if celda_actual == fin:
            break

        #agregamos la celda en que estamos al set de visitadas para no volver atras
        visitados.add(celda_actual)

        #iteramos la lista de celdas transitables, llamando a cada celda como vecino
        for vecino in celdas_transitables(tablero, celda_actual):

            #si ya visitamos esa celda seguimos al siguiente elemento de vecinos por visitar
            if vecino in visitados:
                continue
            
            #gaurdamos el costo actual que sacaremos del diccionario de costo que tenemos, usamos la clave-valor, o sea, sacamos el
            #elemento que se encuentra en el indice celda_actual del diccionario
            costo_actual = diccionario_costos[celda_actual]

            #hallamos el costo de la celda vecina (vemos si es agua o camino)
            costo_celda = tablero[vecino[1], vecino[0]]

            # Si el peso es 0, lo tratamos como 1 para que cuente como un paso
            if costo_celda == 0:
                costo_celda = 1

            #tomamos el costo que han tenido los pasos hasta ahora y lo sumamos a la posible celda a la que nos moveremos
            costo_nuevo = costo_actual + costo_celda

            #vemos si el vecino no ha sido visitado antes, y vemos si el costo de movernos aqui es menor al anterior que probamos
            if vecino not in diccionario_costos or costo_nuevo < diccionario_costos[vecino]:

                #guardamos el costo minimo que nos tomo llegar a esa celda
                diccionario_costos[vecino] = costo_nuevo

                #guardamos la ruta para mostrarla luego
                diccionario_padres[vecino] = celda_actual

                #hallamos la prioridad para ese vecino
                prioridad = costo_nuevo + heuristica(vecino, fin)

                #agregamos ese elemento a la cola
                heapq.heappush(cola_prioridad, (prioridad, vecino))

    #cuando lleguemos al fin, llamamos a la funcion que nos mostrara el camino
    if celda_actual == fin:
        return reconstruir_camino(diccionario_padres, inicio, fin)
    else:
        #si no hallamos camino, no retornamos nada
        return None


def reconstruir_camino(diccionario_padres, inicio, fin):

    #hacemos una lista de las coordenadas de los nodos del camino encontrado
    camino = []

    #vamos desde atras hacia adelante
    actual = fin

    #se ejecuta mientras no estemos en las coordenadas de inicio
    while actual != inicio:

        #agregamos la coordenada acutual
        camino.append(actual)

        #vamos un paso atras para formar el camino
        actual = diccionario_padres[actual]

    #agregamos el nodo de incio
    camino.append(inicio)

    #invertimos la lista
    camino.reverse()

    #retornamos el camino a seguir
    return camino


def imprimir_tablero(tablero):
    for fila in tablero:
        elementos = []
        for x in fila:
            if x == 0:
                elementos.append("🟨")  # camino
            elif x == 9:
                elementos.append("⬛")  # montaña
            elif x == 5:
                elementos.append("🟦")  # agua
            elif x == 7:
                elementos.append("🔴")  # camino encontrado
        print(" ".join(elementos))


def programa_principal():
    tablero = np.array([
        [0, 0, 0, 0, 9, 9, 0, 0, 5, 0],
        [0, 9, 9, 0, 9, 0, 0, 5, 5, 0],
        [0, 0, 0, 0, 9, 0, 9, 9, 5, 0],
        [5, 5, 9, 0, 0, 0, 0, 9, 0, 0],
        [0, 9, 9, 9, 9, 5, 0, 0, 0, 9],
        [0, 0, 0, 0, 5, 0, 0, 9, 0, 0],
        [0, 5, 9, 0, 5, 5, 0, 0, 0, 0],
        [0, 0, 9, 0, 0, 9, 9, 9, 5, 0],
        [9, 0, 0, 0, 0, 0, 0, 5, 5, 0],
        [0, 0, 9, 9, 9, 0, 0, 0, 9, 0],
    ])

    inicio = (0, 0)
    fin = (9, 9)

    camino = a_estrella(inicio, fin, tablero)

    if camino:
        for x, y in camino:
            tablero[y, x] = 7
    else:
        print("No se encontró camino.")

    imprimir_tablero(tablero)


programa_principal()
