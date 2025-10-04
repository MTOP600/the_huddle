# IMPORTAMOS LAS LIBRERÍAS NECESARIAS
import numpy as np
import os
import heapq
import time
import os
import sys

# --- CLASE PARA INGRESAR DATOS ---
class Ingreso_De_Datos:

    def ingreso_dimensiones_tablero(self):
        while True:
            try:
                filas = int(input("Ingrese el número de filas del tablero: "))
                columnas = int(input("Ingrese el número de columnas del tablero: "))
                if filas <= 0 or columnas <= 0:
                    print("Las dimensiones deben de ser mayores que 0")
                    continue
                self.filas = filas
                self.columnas = columnas
                break
            except ValueError:
                print("Ingrese numeros enteros mayores que cero.")

    def ingreso_coordenadas(self, tablero):
        while True:
            coordenada_x = int(input("Ingrese coordenada en x: "))
            coordenada_y = int(input("Ingrese coordenada en y: "))

            if 0 <= coordenada_x < self.filas and 0 <= coordenada_y < self.columnas:
                self.coordenada_x = coordenada_x
                self.coordenada_y = coordenada_y
                break
            else:
                print('Coordenadas se salen del mapa, ingrese nuevamente.')

    def tipo_de_obstaculo(self):
        while True:
            tipo = input(
                '--- SELECCIONE EL TIPO DE OBSTÁCULO ---\n'
                '"c" para camino\n'
                '"t" para tierra\n'
                '"a" para agua\n'
                '"m" para montaña\n'
                'Ingrese opción: '
            ).lower().strip()

            if tipo == 'c':
                self.peso = 1
                break
            elif tipo == 't':
                self.peso = 3
                break
            elif tipo == 'a':
                self.peso = 7
                break
            elif tipo == 'm':
                self.peso = 9
                break
            else:
                print('Dato inválido, intente nuevamente.')


# --- CLASE TABLERO ---
class Tablero(Ingreso_De_Datos):
    def __init__(self):
        super().__init__()
        self.ingreso_dimensiones_tablero()
        self.tablero = np.ones((self.filas, self.columnas), dtype=int)
        self.coordenada_x = None
        self.coordenada_y = None

    def imprimir_tablero(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                valor = self.tablero[i, j]
                if valor == 1:
                    fila.append('.')
                elif valor == 3:
                    fila.append('H')
                elif valor == 7:
                    fila.append('~')
                elif valor == 9:
                    fila.append('X')
                elif valor == 0:
                    fila.append('*')  # Camino encontrado
            print(' '.join(fila))
        print('')

    def colocar_obstaculos(self):
        while True:
            modo = input('Ingrese "a" para agregar obstáculo o "s" para salir: ').lower().strip()
            if modo == 'a':
                self.ingreso_coordenadas(self.tablero)
                self.tipo_de_obstaculo()
                self.tablero[self.coordenada_x, self.coordenada_y] = self.peso
                self.imprimir_tablero()
            elif modo == 's':
                print("Ingrese coordenadas del punto de inicio.")
                self.ingreso_coordenadas(self.tablero)
                self.inicio = (self.coordenada_x, self.coordenada_y)

                print("Ingrese coordenadas del punto de fin.")
                self.ingreso_coordenadas(self.tablero)
                self.fin = (self.coordenada_x, self.coordenada_y)
                break
            else:
                print("Opción inválida. Intente nuevamente.")


# --- CLASE BUSCADOR DE RUTA (A*) ---
class Buscador_De_Ruta:
    def __init__(self, tablero):
        self.tablero = tablero
        self.inicio = tablero.inicio
        self.fin = tablero.fin

    def heuristica(self, coordenada):
        # Distancia Manhattan
        return abs(coordenada[0] - self.fin[0]) + abs(coordenada[1] - self.fin[1])

    def coordenadas_disponibles(self, coordenada):
        direcciones = [(1,0),(0,1),(-1,0),(0,-1)]
        disponibles = []

        for dx, dy in direcciones:
            nx, ny = coordenada[0] + dx, coordenada[1] + dy
            if 0 <= nx < self.tablero.filas and 0 <= ny < self.tablero.columnas:
                if self.tablero.tablero[nx, ny] != 9:  # No puede pasar por montaña
                    disponibles.append((nx, ny))
        return disponibles

    def a_estrella(self):
        cola = []
        heapq.heappush(cola, (0, self.inicio))
        costos = {self.inicio: 0}
        padres = {}

        while cola:
            _, actual = heapq.heappop(cola)

            if actual == self.fin:
                self.reconstruir_camino(padres)
                return

            for vecino in self.coordenadas_disponibles(actual):
                nuevo_costo = costos[actual] + self.tablero.tablero[vecino[0], vecino[1]]

                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    prioridad = nuevo_costo + self.heuristica(vecino)
                    heapq.heappush(cola, (prioridad, vecino))
                    padres[vecino] = actual

        print("No se encontró un camino disponible.")

    def reconstruir_camino(self, padres):
        actual = self.fin
        camino = []

        while actual != self.inicio:
            camino.append(actual)
            actual = padres[actual]
        camino.append(self.inicio)
        camino.reverse()

        print("Camino encontrado:", camino)
        print("")

        # Marcar camino en el tablero
        for (x, y) in camino:
            if (x, y) not in (self.inicio, self.fin):
                self.tablero.tablero[x, y] = 0  # Marcar con *

        self.tablero.imprimir_tablero()


# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    tablero = Tablero()
    tablero.colocar_obstaculos()

    buscador = Buscador_De_Ruta(tablero)
    buscador.a_estrella()
