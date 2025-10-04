# app.py
import tkinter as tk
import numpy as np
import heapq
import time
import os
import sys

# --- CLASE PARA INGRESAR DATOS ---
class Ingreso_De_Datos:
    def ingreso_dimensiones_tablero(self):
        # pedimos dimensiones por consola antes de iniciar la GUI
        while True:
            try:
                filas = int(input("Ingrese el número de filas del tablero: "))
                columnas = int(input("Ingrese el número de columnas del tablero: "))
                if filas <= 0 or columnas <= 0:
                    print("Las dimensiones deben ser mayores que 0.")
                    continue
                self.filas = filas
                self.columnas = columnas
                break
            except ValueError:
                print("Ingrese números enteros válidos.")


# --- CLASE TABLERO (backend + interfaz) ---
class Tablero(Ingreso_De_Datos):
    def __init__(self, root):
        super().__init__()
        self.ingreso_dimensiones_tablero()
        self.root = root

        # backend: pesos
        # por convención: 1 = camino/default, 3 = tierra, 7 = agua, 9 = montaña(no transitable), 0 = camino encontrado
        self.tablero = np.ones((self.filas, self.columnas), dtype=int)

        # GUI
        self.botones = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        self.estado = 'inicial'  # 'inicial', 'seleccionando_inicio', 'seleccionando_fin', 'listo', 'editando_obstaculos', 'editando'
        self.inicio = None  # (fila, col)
        self.fin = None

        self._build_ui()

    def _build_ui(self):
        self.root.title("Calculadora de caminos - A*")
        # estado / instrucciones
        self.label_estado = tk.Label(self.root, text="Edite el mapa (clic: ciclo de terreno). Luego presione 'Listo'")
        self.label_estado.grid(row=0, column=0, columnspan=self.columnas, pady=(5, 5))

        # grid de botones (fila, columna)
        for i in range(self.filas):
            for j in range(self.columnas):
                b = tk.Button(self.root, width=3, height=1, bg='tan',
                              command=lambda r=i, c=j: self.cambiar_color(r, c))
                b.grid(row=i+1, column=j, padx=0, pady=0)
                self.botones[i][j] = b

        # boton principal
        self.boton_listo = tk.Button(self.root, text='Listo', command=self.mapa_terminado)
        self.boton_listo.grid(row=self.filas+2, column=0, columnspan=self.columnas, sticky='nsew', pady=8)

        # boton para reiniciar completamente
        self.boton_reiniciar = tk.Button(self.root, text='Reiniciar mapa', command=self.reiniciar_mapa)
        self.boton_reiniciar.grid(row=self.filas+3, column=0, columnspan=self.columnas, sticky='nsew', pady=(0,8))

        # inicializacion visual según valores (todos 1)
        self._repintar_tablero()

    def _repintar_tablero(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                self._aplicar_color_button(i, j)

        # marcar inicio/fin si existen
        if self.inicio:
            r, c = self.inicio
            self.botones[r][c].config(bg='green')
        if self.fin:
            r, c = self.fin
            self.botones[r][c].config(bg='red')

    def _aplicar_color_button(self, i, j):
        val = self.tablero[i, j]
        btn = self.botones[i][j]
        # mapping de colores (ajustable)
        if val == 1:
            btn.config(bg='tan')      # camino por defecto
        elif val == 3:
            btn.config(bg='peru')     # tierra (más costosa)
        elif val == 7:
            btn.config(bg='navy')     # agua (aún más costosa)
        elif val == 9:
            btn.config(bg='grey')     # montaña (no transitable)
        elif val == 0:
            btn.config(bg='orange')   # camino encontrado
        elif val == 5:
            btn.config(bg='blue')     # obstáculo tipo alterno (si lo usas)
        else:
            btn.config(bg='tan')

    def cambiar_color(self, i, j):
        """
        Comportamiento por estado:
        - inicial / editando: ciclo de tipos de terreno cada click
        - seleccionando_inicio: set inicio (fila,col)
        - seleccionando_fin: set fin (fila,col)
        """
        if self.estado in ('inicial', 'editando', 'editando_obstaculos'):
            actual = int(self.tablero[i, j])
            # ciclo: 1 -> 3 -> 7 -> 9 -> 1
            if actual == 1:
                self.tablero[i, j] = 3
            elif actual == 3:
                self.tablero[i, j] = 7
            elif actual == 7:
                self.tablero[i, j] = 9
            elif actual == 9:
                self.tablero[i, j] = 1
            elif actual == 0:
                # si era camino encontrado y el usuario edita lo volvemos a default
                self.tablero[i, j] = 1
            else:
                self.tablero[i, j] = 1
            self._aplicar_color_button(i, j)

        elif self.estado == 'seleccionando_inicio':
            # si hay inicio anterior, repintarlo según su peso (no dejarlo verde)
            if self.inicio is not None:
                pr, pc = self.inicio
                self._aplicar_color_button(pr, pc)
            self.inicio = (i, j)
            self.botones[i][j].config(bg='green')
            self.label_estado.config(text=f"Inicio: {self.inicio}. Ahora seleccione el fin.")
            self.estado = 'seleccionando_fin'

        elif self.estado == 'seleccionando_fin':
            if self.fin is not None:
                pr, pc = self.fin
                self._aplicar_color_button(pr, pc)
            self.fin = (i, j)
            self.botones[i][j].config(bg='red')
            self.label_estado.config(text=f"Fin: {self.fin}. Presione 'Listo' para hallar el camino.")
            self.estado = 'listo'

    def mapa_terminado(self):
        """
        Accion del boton 'Listo' segun estado:
        - si inicial => pasar a seleccionar inicio
        - si listo => ejecutar busqueda
        - si editando_obstaculos => volver a modo editando
        - si editando => recalcular
        """
        if self.estado == 'inicial':
            self.estado = 'seleccionando_inicio'
            self.label_estado.config(text='Seleccione el inicio en el tablero')
            self.boton_listo.config(text='Reiniciar selección')
        elif self.estado == 'seleccionando_inicio':
            # seguro
            self.label_estado.config(text='Seleccione el inicio en el tablero')
            self.estado = 'seleccionando_inicio'
        elif self.estado == 'seleccionando_fin':
            # todavía esperando fin
            self.label_estado.config(text='Seleccione el fin en el tablero')
        elif self.estado == 'listo':
            # lanzamos el A*
            self.boton_listo.config(text='Calculando...')
            self.root.update()
            buscador = Buscador_De_Ruta(self)
            camino = buscador.a_estrella_visual()
            if camino:
                # marcar camino en tablero backend (0) excepto inicio y fin
                for (r, c) in camino:
                    if (r, c) != self.inicio and (r, c) != self.fin:
                        self.tablero[r, c] = 0
                self._repintar_tablero()
                self.label_estado.config(text='Camino encontrado. Puede editar el mapa y recalcular.')
                self.estado = 'editando_obstaculos'
                self.boton_listo.config(text='Agregar obstáculos')
            else:
                self.label_estado.config(text='No se encontró camino. Puede editar el mapa y volver a intentar.')
                self.estado = 'editando_obstaculos'
                self.boton_listo.config(text='Agregar obstáculos')
        elif self.estado == 'editando_obstaculos':
            self.estado = 'editando'
            self.label_estado.config(text='Edite el mapa y presione "Listo" para recalcular')
            self.boton_listo.config(text='Recalcular camino')
        elif self.estado == 'editando':
            # recalcular
            self.boton_listo.config(text='Calculando...')
            self.root.update()
            buscador = Buscador_De_Ruta(self)
            camino = buscador.a_estrella_visual()
            if camino:
                for (r, c) in camino:
                    if (r, c) != self.inicio and (r, c) != self.fin:
                        self.tablero[r, c] = 0
                self._repintar_tablero()
                self.label_estado.config(text='Camino encontrado. Puede seguir editando.')
                self.estado = 'editando_obstaculos'
                self.boton_listo.config(text='Agregar obstáculos')
            else:
                self.label_estado.config(text='No se encontró camino. Puede editar el mapa y volver a intentar.')
                self.estado = 'editando_obstaculos'
                self.boton_listo.config(text='Agregar obstáculos')

    def reiniciar_mapa(self):
        # reinicia totalmente
        self.tablero[:] = 1
        self.inicio = None
        self.fin = None
        self.estado = 'inicial'
        self.boton_listo.config(text='Listo')
        self.label_estado.config(text='Edite el mapa (clic: ciclo de terreno). Luego presione "Listo"')
        self._repintar_tablero()


# --- CLASE BUSCADOR (A* con visualización) ---
class Buscador_De_Ruta:
    def __init__(self, tablero_obj: Tablero):
        self.tablero_obj = tablero_obj
        self.tab = tablero_obj.tablero
        self.root = tablero_obj.root
        self.filas = tablero_obj.filas
        self.columnas = tablero_obj.columnas
        self.inicio = tablero_obj.inicio
        self.fin = tablero_obj.fin

    def heuristica(self, a, b):
        # Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def vecinos_validos(self, nodo):
        r, c = nodo
        direcciones = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        resultado = []
        for dr, dc in direcciones:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.filas and 0 <= nc < self.columnas:
                if self.tab[nr, nc] != 9:  # no transitable si montaña
                    resultado.append((nr, nc))
        return resultado

    def a_estrella_visual(self):
        if self.inicio is None or self.fin is None:
            self.tablero_obj.label_estado.config(text="Primero seleccione inicio y fin")
            return None

        inicio = self.inicio
        fin = self.fin

        cola = []
        heapq.heappush(cola, (0, inicio))
        costos = {inicio: 0}
        padres = {}
        visitados = set()

        # animación: cada vez que se expande un nodo se repinta (excepto inicio/fin)
        while cola:
            prioridad, actual = heapq.heappop(cola)

            if actual in visitados:
                continue
            visitados.add(actual)

            # mostrar exploración (si no es inicio/fin)
            if actual != inicio and actual != fin:
                ar, ac = actual
                # solo cambiar color temporalmente si no es camino ni otros tipos especiales
                self.tablero_obj.botones[ar][ac].config(bg='brown')
                self.root.update()
                time.sleep(0.02)

            if actual == fin:
                # reconstruir camino
                camino = []
                nodo = fin
                while nodo != inicio:
                    camino.append(nodo)
                    nodo = padres.get(nodo)
                    if nodo is None:
                        break
                if nodo is None:
                    return None
                camino.append(inicio)
                camino.reverse()
                return camino

            for vecino in self.vecinos_validos(actual):
                if vecino in visitados:
                    continue
                costo_actual = costos[actual]
                peso_vecino = int(self.tab[vecino[0], vecino[1]])
                # si hay celdas marcadas como 0 (camino previo) tratarlas como costo 1 para el algoritmo
                if peso_vecino == 0:
                    peso_vecino = 1
                nuevo_costo = costo_actual + peso_vecino

                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    prioridad_vecino = nuevo_costo + self.heuristica(vecino, fin)
                    heapq.heappush(cola, (prioridad_vecino, vecino))
                    padres[vecino] = actual

        # si terminamos la cola y no encontramos fin
        return None


# --- PROGRAMA PRINCIPAL ---
def main():
    # limpiar consola en caso de Windows/Unix
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        pass

    # iniciar GUI (pero dimensiones se piden dentro de Tablero)
    root = tk.Tk()
    # ocultar momentáneamente la ventana mientras pedimos por consola (opcional)
    root.withdraw()
    tablero_obj = Tablero(root)
    # ahora mostrar ventana
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    main()
