#importamos las librerias que vamos a usar
import heapq, numpy as np, tkinter as tk, time

#creamos una funcion de heuristica para el a*
def heuristica(inicio, fin):
    #desempaquetamos las coordenadas de los extremos
    inicio_x, inicio_y = inicio
    fin_x, fin_y = fin
    #retornamos el resultado de la distancia euclidiana
    return abs(inicio_x - fin_x) + abs(inicio_y - fin_y)

#creamos una funcion a la que se le pasa la coordenada de una celda y devuelve las celdas transitables
def celdas_transitables(tablero, celda_actual):
    #desempaquetamos las coordenadas de la celda a la que le            hallaremos las celdas adyacentes transitables
    actual_x, actual_y = celda_actual
    #creamos una lista para devolver las celdas a las que nos podemos mover
    direcciones_disponibles = []
    #creamos una lista de tuplas con las direcciones a las que probar 
    movimientos = [(0,1), (1,0), (0,-1), (-1,0)]
    #con .shape lo que hacemos es hallas las dimensiones del tablero
    filas, columnas = tablero.shape
    #iteramos la lista y probamos cada celda adyacente para saber si es valida
    for dx, dy in movimientos:
        #sumamos la dirección del movimiento a cada coordenada
        posible_x = actual_x + dx
        posible_y = actual_y + dy
        #nos aseguramos de no salirnos del tablero
        if 0 <= posible_x < columnas and 0 <= posible_y < filas:
            peso = tablero[posible_y, posible_x]
            #nos aseguramos de que no sea una pared
            if peso != 9:  # 9 = montaña, no transitable
                direcciones_disponibles.append((posible_x, posible_y))
    #cuando hallamos todas las disponibles, retornamos una lista con las coordenadas 
    return direcciones_disponibles

#creamos una función exclusiva para el algoritmo de búsqueda de caminos
def a_estrella(inicio, fin, tablero):
    #tomamos las variables globales de tkinter
    global botones, root
    #creamos una lista de caminos con prioridad de prueba que se basará en la heuristica
    cola_prioridad = []
    #usamos la heuristica para hallar una prioridad a la primera celda
    heuristica_inicio = heuristica(inicio, fin)
    #ordenamos la lista basándonos en la heuristica más pequeña (celda más prometedora)
    heapq.heappush(cola_prioridad, (heuristica_inicio, inicio))
    #creamos un diccionario al que cada celda tendrá x costo de llegar hasta ahí desde el inicio
    diccionario_costos = {inicio: 0}
    #creamos un diccionario de padres que sirve para reconstruir el camino, (cada celda {valor} apunta a la celda de donde salió {clave})
    diccionario_padres = {}
    #hacemos un set (no duplicados), para las celdas que ya probamos y no hacer más trabajo del necesario 
    visitados = set()
    #este while se ejecuta mientras la cola_prioridad tenga elementos
    while cola_prioridad:
        #ignoramos la heuristica y tomamos la celda con más prioridad actualmente 
        _, celda_actual = heapq.heappop(cola_prioridad)
        #desempaquetamos la coordenada de dicha celda
        x, y = celda_actual
        #verificamos que no sea la celda de inicio ni la de fin (esto es para ver el proceso de búsqueda de a*, cada que este sobre una celda cambiará el color a uno ligeramente más oscuro)
        if celda_actual != inicio and celda_actual != fin:
            if tablero[y,x]==0:
                botones[y][x].config(bg='brown')
            elif tablero[y,x]==5:
                botones[y][x].config(bg='navy')
            elif tablero[y,x]==9:
                botones[y][x].config(bg='black')
            #le decimos a tkinter que actualice los colores que acabamos de cambiar
            root.update()
            #para que espere un poco y el proceso sea visible 
            time.sleep(0.05)
        #en caso de que haya un camino y logremos llegar a la celda fin, llamamos a la función de reconstruir camino
        if celda_actual == fin:
            return reconstruir_camino(diccionario_padres, inicio, fin)
        #si no, marcamos la celda como visitada
        visitados.add(celda_actual)
        #iteramos las celdas que podemos visitar (celdas_transitables ahora es una lista de tuplas y cada tupla es la coordenada de una celda transitable)
        for vecino in celdas_transitables(tablero, celda_actual):
            #si ya visitamos esa celda, continuamos con las siguientes en la lista de transitables 
            if vecino in visitados:
                continue
            #vemmos cuánto nos cuesta llegar hasta aquí desde el punto de inicio
            costo_actual = diccionario_costos[celda_actual]
            #vemos que peso tiene el vecino que estamos probando (cuánto más nos costará movernos a esa celda)
            costo_vecino = tablero[vecino[1], vecino[0]]
            #esto es más un parche, si el costo fuera 0, el algoritmo fallaría, ya que siempre priorizaría esa celda hasta incluso si no es la más conveniente, así que la cambiamos a 1)
            if costo_vecino == 0:
                costo_vecino = 1
            #ahora vemos cuánto nos cuesta movernos desde el inicio del tablero hasta esa celda vecina
            costo_nuevo = costo_actual + costo_vecino
            #si nuestro vecino aún no tiene un valor en diccionario costos, o hallamos que moviendonos desde otra celda adyacente, tiene un menor valor, le asignamos ese valor menor
            if vecino not in diccionario_costos or costo_nuevo < diccionario_costos[vecino]:
                #a ese vecino le ponemos lo que nos cuesta llegar hasta ahí desde el incio
                diccionario_costos[vecino] = costo_nuevo
                #guardamos como llegamos a ese vecino desde el inicio del tablero (el camino que seguimos)
                diccionario_padres[vecino] = celda_actual
                #le asignamos una prioridad a esa celda (que tan prometedor es llegar hasta ahí)
                prioridad = costo_nuevo + heuristica(vecino, fin)
                #ordenamos la cola de prioridad con el calor de ese vecino en vase a la prioridad que le asignamos recién 
                heapq.heappush(cola_prioridad, (prioridad, vecino))
    # ver después 
    return None
#funcion exclusiva para ver el camino que conecta el inicio con el fin
def reconstruir_camino(diccionario_padres, inicio, fin):
    #creamos una lista que representará los pasos dados desde el inicio hasta el fin (el camino)
    camino = []
    #vamos a empezar a reconstruir el camino desde el fin del tablero (necesariamente ya que usando el diccionario debe llegar al inicio del tablero, ya que desde ahí empezamos a armarlo)
    actual = fin
    #mientras la celda que estamos recorriendo sea diferente al inicio del tablero 
    while actual != inicio:
        #agregamos la celda actual al camino 
        camino.append(actual)
        #vemos desde donde hicimos el paso para llegar a esa celda
        actual = diccionario_padres[actual]
    #cuando recorramos todo el camino, agregamos la celda incio a la lista
    camino.append(inicio)
    #invertimos los elementos de la lista (antes era de atrás para adelante, ahora es de adelante para atrás)
    camino.reverse()
    #retornamos el camino que hallamos
    return camino

#para mostrar el laberinto, esto se encarga de cambiar los colores de los botones en la interfaz gráfica 
def cambiar_color(i, j):
    #tomamos todas estas variables como globales 
    global estado, inicio, fin, tablero, botones, label_estado
    #en base a cada peso que tiene el tablero le vamos a pintar un color al botón 
    if estado == "inicial" or estado == "editando":
        if tablero[i, j] == 0:
            tablero[i, j] = 5
            botones[i][j].config(bg="blue")
        elif tablero[i, j] == 5:
            tablero[i, j] = 9
            botones[i][j].config(bg="grey")
        elif tablero[i, j] == 9:
            tablero[i, j] = 0
            botones[i][j].config(bg="tan")
   #pintaremos el botón de inicio que se seleccione con el color verde
    elif estado == "seleccionando_inicio":
        inicio = (j, i)
        botones[i][j].config(bg="green")
        #luego de cambiar el color, ponemos el estado en seleccionando fin, para que el botón correspondiente se pinte de color rojo 
        label_estado.config(text=f"Inicio: {inicio}. Ahora seleccione el fin.")
        estado = "seleccionando_fin"

    #pintamos el botón de fin con el color rojo
    elif estado == "seleccionando_fin":
        fin = (j, i)
        botones[i][j].config(bg="red")
        label_estado.config(text=f"Fin: {fin}. Ahora presione el botón de abajo para hallar el camino.")
        estado = "listo"
#esto controla los estados del mapa para que el programa actúe de diferentes formas
def mapa_terminado():
    #declaramos las variables necesarias como globales
    global estado, tablero, inicio, fin
    #cuando ya editamos todo
    if estado == 'inicial':
        #cambiamos el estado a seleccionando inicio 
        estado = 'seleccionando_inicio'
        #le decimos al usuario que seleccione el botón que será el incio 
        label_estado.config(text='Seleccione el inicio en el tablero')
        #para resetear 
        boton_listo.config(text='Reiniciar')

    #si ya quiere hallar el camino
    elif estado == 'listo':
        calcular_camino()

#para luego de la primera ejecución 
    elif estado == 'editando_obstaculos':
        estado = 'editando'
        label_estado.config(text="Edite el mapa y luego presione Listo para recalcular")
        boton_listo.config(text="Recalcular camino")

#cuando edite todo el mapa
    elif estado == 'editando':
        calcular_camino()
#para resetear el mapa
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

#esto se usara cada que queramos hallar el camino
def calcular_camino():
    global inicio, fin, tablero, estado
    #si no se ha seleccionado el inicio o el fin, no ejecutamos el algoritmo 
    if inicio is None or fin is None:
        label_estado.config(text="Primero seleccione inicio y fin")
        return
    #llamamos a el algoritmo de búsqueda 
    camino = a_estrella(inicio, fin, tablero)
    #si halla un camino, nos devolverá la lista de las celdas que forma el camino, iteramos entre ellas 
    if camino:
        # repintar tablero sin borrar inicio y fin
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
     
        # dibujar nuevo camino, pintamos las celdas que forman el camino de color naranja 
        for x, y in camino:
            if (x,y) != inicio and (x,y) != fin:
                botones[y][x].config(bg='orange')
        #cuando ya mostramos el camino encontrado, le decimos al usuario que puede editar el mapa
        label_estado.config(text='Camino encontrado, puede agregar más obstáculos')
        
        boton_listo.config(text='Agregar obstáculos')
        estado = 'editando_obstaculos'
        #esto es para debug
        print('Matriz final:\n', tablero)
    #si no tenemos una lista de caminos
    else:
        label_estado.config(text='No se encontró camino.')

#variables globales que se usan en todo el programa 
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
    #pedimos que se ingresen las dimensiones del tablero
    filas = int(input("Ingrese el numero de filas del tablero:"))
    columnas = int(input("Ingrese el numero de columnas del tablero:"))
   
    #creamos el tablero 
    tablero = np.zeros((filas, columnas), dtype=int)
    #lista de botones para tkinter
    botones = []
    #switch de estado en incial
    estado = 'inicial'
    #no tenemos inicio ni fin aún 
    inicio = None
    fin = None
    #creamos una variable que será la ventana de tkinter
    root = tk.Tk()
    root.title('Calculadora de caminos')

    #decimos que pinte los obstáculos 
    label_estado = tk.Label(root, text='Seleccione un punto en el mapa')
    label_estado.grid(row=0, column=0, columnspan=columnas)
    #recorremos la matriz y vamos armando la interfaz en base a esl
    for i in range(filas):
        fila = []
        for j in range(columnas):
            boton = tk.Button(root, width=3, height=1, bg="tan",
                  command=lambda x=i, y=j: cambiar_color(x, y))
            boton.grid(row=i+1, column=j)
            fila.append(boton)
        botones.append(fila)

    boton_listo = tk.Button(root, text='Listo', command=mapa_terminado)
    boton_listo.grid(row=filas+2, column=0, columnspan=columnas, sticky='nsew', pady=10)
    #para inicializar toda la interfaz 
    root.mainloop()

#para correr el programa principal 
programa_principal()
