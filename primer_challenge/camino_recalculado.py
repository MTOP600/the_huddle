#importamos las librerias que vamos a usar
import heapq, numpy as np, tkinter as tk, time

#creamos una funcion de heuristica para el a*
def heuristica(inicio, fin):
    inicio_x, inicio_y = inicio
    fin_x, fin_y = fin
    return abs(inicio_x - fin_x) + abs(inicio_y - fin_y)

#creamos una funcion a la que se le pasa la coordenada de una celda y devuelve las celdas transitables
def celdas_transitables(tablero, celda_actual):
    actual_x, actual_y = celda_actual
    direcciones_disponibles = []
    movimientos = [(0,1), (1,0), (0,-1), (-1,0)]
    filas, columnas = tablero.shape

    for dx, dy in movimientos:
        posible_x = actual_x + dx
        posible_y = actual_y + dy
        if 0 <= posible_x < columnas and 0 <= posible_y < filas:
            peso = tablero[posible_y, posible_x]
            if peso != 9:  # 9 = montaña, no transitable
                direcciones_disponibles.append((posible_x, posible_y))
    return direcciones_disponibles

def a_estrella(inicio, fin, tablero):
    global botones, root
    cola_prioridad = []
    heuristica_inicio = heuristica(inicio, fin)
    heapq.heappush(cola_prioridad, (heuristica_inicio, inicio))
    diccionario_costos = {inicio: 0}
    diccionario_padres = {}
    visitados = set()

    while cola_prioridad:
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
            time.sleep(0.05)

        if celda_actual == fin:
            return reconstruir_camino(diccionario_padres, inicio, fin)

        visitados.add(celda_actual)
        for vecino in celdas_transitables(tablero, celda_actual):
            if vecino in visitados:
                continue
            costo_actual = diccionario_costos[celda_actual]
            costo_vecino = tablero[vecino[1], vecino[0]]
            if costo_vecino == 0:
                costo_vecino = 1
            costo_nuevo = costo_actual + costo_vecino
            if vecino not in diccionario_costos or costo_nuevo < diccionario_costos[vecino]:
                diccionario_costos[vecino] = costo_nuevo
                diccionario_padres[vecino] = celda_actual
                prioridad = costo_nuevo + heuristica(vecino, fin)
                heapq.heappush(cola_prioridad, (prioridad, vecino))
    return None

def reconstruir_camino(diccionario_padres, inicio, fin):
    camino = []
    actual = fin
    while actual != inicio:
        camino.append(actual)
        actual = diccionario_padres[actual]
    camino.append(inicio)
    camino.reverse()
    return camino

#para mostrar el laberinto
def cambiar_color(i, j):
    global estado, inicio, fin, tablero, botones, label_estado

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

    elif estado == "seleccionando_inicio":
        inicio = (j, i)
        botones[i][j].config(bg="green")
        label_estado.config(text=f"Inicio: {inicio}. Ahora seleccione el fin.")
        estado = "seleccionando_fin"

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

    elif estado == 'editando_obstaculos':
        estado = 'editando'
        label_estado.config(text="Edite el mapa y luego presione Listo para recalcular")
        boton_listo.config(text="Recalcular camino")

    elif estado == 'editando':
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

# --- Variables globales ---
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

    filas = int(input("Ingrese el numero de filas del tablero:"))
    columnas = int(input("Ingrese el numero de columnas del tablero:"))

    tablero = np.zeros((filas, columnas), dtype=int)
    botones = []
    estado = 'inicial'
    inicio = None
    fin = None

    root = tk.Tk()
    root.title('Calculadora de caminos')

    label_estado = tk.Label(root, text='Seleccione un punto en el mapa')
    label_estado.grid(row=0, column=0, columnspan=columnas)

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

    root.mainloop()

programa_principal()
