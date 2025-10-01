#importamos las librerias que vamos a usar
import heapq, numpy as np, tkinter as tk, time

#creamos una funcion de heuristica para el a*
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

def a_estrella(inicio, fin, tablero):
    global botones, root

    #hacemos una cola para probar las direcciones
    cola_prioridad = []

    #la heuristica sirve como una brujula que nos dice mas o menos hacia donde debemos probar
    heuristica_inicio = heuristica(inicio, fin)

    #esto es un monticulo, lo que estamos haciendo es organizar la cola_prioridad en base a el numero heuristica, lo que hace es ordenar
    #la lista cola_prioridad de menor a mayor, haciendonos mas facil tomar la decision de hacia donde movernos (heuristica mas pequena,
    #movimiento mas conveniente), el elemento con menor valor de  heuristica esta siempre en la raiz de la cola
    heapq.heappush(cola_prioridad, (heuristica_inicio, inicio))

    #diccionario con lo que nos cuesta movernos hasta x celda, cargamos la celda inicial
    diccionario_costos = {inicio: 0}

    #usamos esto para luego volver sobre nuestros pasos y hallar el camino, cada nueva celda apunta hacia la celda del paso anterior
    diccionario_padres = {}

    #inicializamos un set de visitados para no quedar en bucles infinitos
    visitados = set()

    #hacemos un while que se ejecuta siempre que haya lugares a los que movernos
    while cola_prioridad:

        #obetenemos el primer elemento (heuristica mas pequena) de la tupla cola_prioridad, ignoramos el valor de la heuristica con _ ya que no lo vamos a usar
        #aqui, solamente nos interesa celda actual
        _, celda_actual = heapq.heappop(cola_prioridad)

        x, y = celda_actual
        if celda_actual != inicio and celda_actual != fin:
            if tablero[y,x]==0:
                botones[y][x].config(bg='brown')
            elif tablero[y,x]==5:
                botones[y][x].config(bg='navy')
            elif tablero[y,x]==9:
                botones[y][x].config(bg='black')
            
            

            root.update()
            time.sleep(0.2)

        #si llegamos al fin, salimos del while
        if celda_actual == fin:
            return reconstruir_camino(diccionario_padres, inicio, fin)

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
            costo_vecino = tablero[vecino[1], vecino[0]]

            # Si el peso es 0, lo tratamos como 1 para que cuente como un paso
            if costo_vecino == 0:
                costo_vecino = 1

            #tomamos el costo que han tenido los pasos hasta ahora y lo sumamos a la posible celda a la que nos moveremos
            costo_nuevo = costo_actual + costo_vecino

            #vemos si el vecino no ha sido visitado antes, y vemos si el costo de movernos aqui es menor al anterior que probamos
            if vecino not in diccionario_costos or costo_nuevo < diccionario_costos[vecino]:

                #guardamos el costo que nos tomo llegar a esa celda
                diccionario_costos[vecino] = costo_nuevo

                #guardamos la ruta para mostrarla luego
                diccionario_padres[vecino] = celda_actual

                #hallamos la prioridad para ese vecino
                prioridad = costo_nuevo + heuristica(vecino, fin)

                #agregamos ese elemento a la cola
                heapq.heappush(cola_prioridad, (prioridad, vecino))

    #Termino el while y no encontro camino, retornamos none
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

#para mostrar el laberinto
def cambiar_color(i, j):

    #sacamos las variables globales para modificarlas de forma definitiva
    global estado, inicio, fin, tablero, botones, label_estado

    #esto es como un switch, dependiendo del estado del tablero, actuara de cierta forma

    #esto es el modo de pintar el mapa
    if estado == "inicial":

        #en base a lo que esta guardado en el tablero, modifiamos los botones de esa coordenada
        if tablero[i, j] == 0:
            tablero[i, j] = 5
            botones[i][j].config(bg="blue")
        elif tablero[i, j] == 5:
            tablero[i, j] = 9
            botones[i][j].config(bg="grey")
        elif tablero[i, j] == 9:
            tablero[i, j] = 0
            botones[i][j].config(bg="tan")
    
    #aqui pintamos el inicio del mapa
    elif estado == "seleccionando_inicio":

        inicio = (j, i)
        botones[i][j].config(bg="green")
        label_estado.config(text=f"Inicio: {inicio}. Ahora seleccione el fin.")
        estado = "seleccionando_fin"

    #aqui pintamos el fin del tablero
    elif estado == "seleccionando_fin":
        fin = (j, i)
        botones[i][j].config(bg="red")
        label_estado.config(text=f"Fin: {fin}. Ahora calcule el camino.")
        estado = "listo"


def mapa_terminado():
    global estado, tablero, inicio, fin

    if estado == 'inicial':
        estado = 'seleccionando_inicio'
        label_estado.config(text='Seleccione el inicio en el tablero')
        boton_listo.config(text='Reiniciar')
    
    elif estado == 'listo':
        calcular_camino()
    
    elif estado=='editando':
        calcular_camino()
    else:
        #reiniciar
        estado = 'inicial'
        tablero = np.zeros((filas, columnas), dtype=int)
        inicio = None
        fin = None
        for i in range(filas):
            for j in range(columnas):
                botones[i][j].config(bg='tan')
        label_estado.config(text='Seleccione un punto en el mapa')
        boton_listo.config(text='Listo')

def calcular_camino():
    global inicio, fin, tablero, estado

    if inicio is None or fin is None:
        label_estado.config(text="Primero seleccione inicio y fin")
        return
    
    camino = a_estrella(inicio, fin, tablero)

    if camino:
        # repintar tablero sin borrar inicio/fin
        for i in range(filas):
            for j in range(columnas):
                if (j,i) == inicio:
                    botones[i][j].config(bg='green')
                elif (j,i) == fin:
                    botones[i][j].config(bg='red')
                elif tablero[i,j] == 5:
                    botones[i][j].config(bg='blue')
                elif tablero[i,j] == 9:
                    botones[i][j].config(bg='grey')
                else:
                    botones[i][j].config(bg='tan')

        # dibujar nuevo camino
        for x, y in camino:
            if (x,y) != inicio and (x,y) != fin:
                botones[y][x].config(bg='orange')

        label_estado.config(text='Camino encontrado, puede agregar más obstáculos')
        boton_listo.config(text='Agregar obstáculos')
          
        estado = 'editando_obstaculos'
        print('Matriz final:\n', tablero)
    else:
        label_estado.config(text='No se encontró camino.')

#def editando_mapa():


filas = 0
columnas = 0
tablero = None
botones = []
estado = ""
inicio = None
fin = None
label_estado = None
boton_listo = None


#PROGRAMA PRINCIPAL
def programa_principal():

    global filas, columnas, tablero, botones, estado, inicio, fin, label_estado, boton_listo, root


    #definimos el tamano del tablero
    filas = int(input("Ingrese el numero de filas del tablero:"))
    columnas = int(input("Ingrese el numero de columnas del tablero:"))

    #incializamos el tablero
    tablero = np.zeros((filas, columnas), dtype=int)

    #los botones de la interfaz grafica
    botones = []

    #variable que nos dice en que estado esta el programa
    estado = 'inicial'

    #ponemos las coordenadas de inicio y fin del tablero
    inicio = None
    fin = None

    #inicializamos la interfaz de tkinter
    root = tk.Tk()
    root.title('Calculadora de caminos')

    label_estado = tk.Label(root, text='Seleccione un punto en el mapa')
    label_estado.grid(row=0, column=0, columnspan=columnas)

    for i in range(filas):

        #hacemos una lista donde iremos guardando los botones
        fila = []

        #recorremos cada elemento de la fila
        for j in range(columnas):

            #incializamos el estado del boton, en la ventana root, con los tamanos, colores y ponemos el estilo desde la funcion
            boton = tk.Button(root, width=3, height=1, bg="tan",
                  command=lambda x=i, y=j: cambiar_color(x, y))


            #vamos dibujando el boton
            boton.grid(row=i+1, column=j)

            #agregamos el boton a la fila
            fila.append(boton)

        #agregamos la fila completa a la columna
        botones.append(fila)

    #creamos el boton cuando el mapa ya este todo, con el comando mapa terminado
    boton_listo = tk.Button(root, text='Listo', command=mapa_terminado)

    boton_listo.grid(row=filas+2, column=0, columnspan=columnas, sticky='nsew', pady=10)

    root.mainloop()

programa_principal()





