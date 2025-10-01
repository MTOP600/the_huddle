import heapq
import numpy as np
import tkinter as tk

# ======================
#  ALGORITMO A*
# ======================
def heuristica(inicio, fin):
    (x1, y1), (x2, y2) = inicio, fin
    return abs(x1 - x2) + abs(y1 - y2)

def celdas_transitables(tablero, celda_actual):
    x, y = celda_actual
    filas, columnas = tablero.shape
    movimientos = [(0,1), (1,0), (0,-1), (-1,0)]
    direcciones = []

    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < columnas and 0 <= ny < filas:
            if tablero[ny, nx] != 9:  # 9 = obstáculo
                direcciones.append((nx, ny))
    return direcciones

def a_estrella(inicio, fin, tablero):
    cola = []
    heapq.heappush(cola, (heuristica(inicio, fin), inicio))
    costos = {inicio: 0}
    padres = {}
    visitados = set()

    while cola:
        _, actual = heapq.heappop(cola)

        if actual == fin:
            return reconstruir_camino(padres, inicio, fin)

        visitados.add(actual)

        for vecino in celdas_transitables(tablero, actual):
            if vecino in visitados:
                continue

            costo_actual = costos[actual]
            costo_vecino = tablero[vecino[1], vecino[0]]
            if costo_vecino == 0:
                costo_vecino = 1  # tratar camino normal como peso 1
            nuevo_costo = costo_actual + costo_vecino

            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                padres[vecino] = actual
                prioridad = nuevo_costo + heuristica(vecino, fin)
                heapq.heappush(cola, (prioridad, vecino))
    return None

def reconstruir_camino(padres, inicio, fin):
    camino = []
    actual = fin
    while actual != inicio:
        camino.append(actual)
        actual = padres[actual]
    camino.append(inicio)
    camino.reverse()
    return camino

# ======================
#  INTERFAZ TKINTER
# ======================
class InterfazAEstrella:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tablero = np.zeros((filas, columnas), dtype=int)
        self.botones = []
        self.estado = "inicial"
        self.inicio = None
        self.fin = None

        self.root = tk.Tk()
        self.root.title("A* en un tablero dinámico con numpy")

        self.label_estado = tk.Label(self.root, text="Seleccione un punto en el mapa")
        self.label_estado.grid(row=0, column=0, columnspan=self.columnas)

        for i in range(filas):
            fila = []
            for j in range(columnas):
                btn = tk.Button(self.root, width=3, height=1, bg="white",
                                command=lambda x=i, y=j: self.cambiar_color(x, y))
                btn.grid(row=i+1, column=j)
                fila.append(btn)
            self.botones.append(fila)

        self.boton_listo = tk.Button(self.root, text="Listo", command=self.mapa_terminado)
        self.boton_listo.grid(row=filas+2, column=0, columnspan=columnas, sticky="nsew", pady=10)

    def cambiar_color(self, i, j):
        if self.estado == "inicial":
            if self.tablero[i, j] == 0:
                self.tablero[i, j] = 5
                self.botones[i][j].config(bg="blue")
            elif self.tablero[i, j] == 5:
                self.tablero[i, j] = 9
                self.botones[i][j].config(bg="black")
            elif self.tablero[i, j] == 9:
                self.tablero[i, j] = 0
                self.botones[i][j].config(bg="white")

        elif self.estado == "seleccionando_inicio":
            self.inicio = (j, i)
            self.botones[i][j].config(bg="green")
            self.label_estado.config(text=f"Inicio: {self.inicio}. Ahora seleccione el fin.")
            self.estado = "seleccionando_fin"

        elif self.estado == "seleccionando_fin":
            self.fin = (j, i)
            self.botones[i][j].config(bg="red")
            self.label_estado.config(text=f"Fin: {self.fin}. Ahora calcule el camino.")
            self.estado = "listo"

    def mapa_terminado(self):
        if self.estado == "inicial":
            self.estado = "seleccionando_inicio"
            self.label_estado.config(text="Seleccione el inicio (celda verde)")
            self.boton_listo.config(text="Reiniciar")

        elif self.estado == "listo":
            self.calcular_camino()

        else:
            # Reiniciar
            self.estado = "inicial"
            self.tablero = np.zeros((self.filas, self.columnas), dtype=int)
            self.inicio = None
            self.fin = None
            for i in range(self.filas):
                for j in range(self.columnas):
                    self.botones[i][j].config(bg="white")
            self.label_estado.config(text="Seleccione un punto en el mapa")
            self.boton_listo.config(text="Listo")

    def calcular_camino(self):
        if self.inicio is None or self.fin is None:
            self.label_estado.config(text="Debe seleccionar inicio y fin")
            return

        camino = a_estrella(self.inicio, self.fin, self.tablero)
        if camino:
            for x, y in camino:
                if (x, y) != self.inicio and (x, y) != self.fin:
                    self.botones[y][x].config(bg="orange")
            self.label_estado.config(text="Camino encontrado.")
            print("Matriz final:\n", self.tablero)
        else:
            self.label_estado.config(text="No se encontró camino.")

    def ejecutar(self):
        self.root.mainloop()


# ======================
#  PROGRAMA PRINCIPAL
# ======================
if __name__ == "__main__":
    filas = int(input("Ingrese número de filas: "))
    columnas = int(input("Ingrese número de columnas: "))

    app = InterfazAEstrella(filas, columnas)
    app.ejecutar()
