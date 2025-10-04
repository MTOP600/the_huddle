#IMPORTAMOS LAS LIBRERIAS NECESARIAS
import numpy as np
import tkinter as tk
import os
import heapq


#---CREAMOS UNA CLASE PARA QUE SE INGRESEN DISTINTOS TIPOS DE DATOS---
class Ingreso_De_Datos:

    #---PARA INICIALIZAR EL TABLERO CON SU TAMANO---
    def ingreso_dimensiones_tablero(self):

        # ---PEDIMOS FILAS Y COLUMNAS---
        self.filas = int(input("Ingrese el numero de filas del tablero: "))
        self.columnas = int(input("Ingrese el numero de columnas del tablero: "))

    #---PARA COLOCAR DIVERSAS COSAS EN ALGUNA COORDENADA---
    def ingreso_coordenadas(self, tablero):

        # --- USAMOS EL WHILE PARA VERIFICAR QUE LOS DATOS INGRESADOS SEAN VALIDOS---
        while True:

            # ---PEDIMOS LAS COORDENADAS POR SEPARADO---
            coordenada_x = int(input("Ingrese coordenada en x: "))
            coordenada_y = int(input("Ingrese coordenada en y: "))

            # ---VERIFICAMOS QUE NO SE SALGA DEL MAPA---
            if coordenada_x >= 0 and coordenada_x < self.filas and coordenada_y >= 0 and coordenada_y <self.columnas:
                    
                    # ---SI TODO ES VALIDO, INSTANCIAMOS LAS VARIABLES---
                    self.coordenada_x = coordenada_x
                    self.coordenada_y = coordenada_y

                    # ---SALIMOS DEL WHILE---
                    break

            else:

                # ---SI LAS COORDENADAS SON INVALIDAS, CONTINUAMOS PIDIENDO---
                print('Coordenadas se salen del mapa, ingrese nuevamente.')

    # ---EN BASE A ESTO SE CARGARA CIERTO PESO EN LA COORDENADA DE LA CELDA DEL TABLERO---
    def tipo_de_obstaculo(self):

        # ---VOLVEMOS A USAR EL WHILE PARA VERIFICAR LA VALIDEZ DE LOS DATOS---
        while True:

            # ---HACEMOS UN INPUT PIDIENDO EL TIPO DE OBSTACULO---
            tipo = input(
            '---SELECCIONE EL TIPO DE OBSTACULO---' \
            '"c" para camino' \
            '"t" para tierra' \
            '"a" para agua' \
            '"m" para montaña: '
            ).lower().strip() # ---HACEMOS ESTO PARA CONVERTIR A MINUSCULA Y BORRAR LOS ESPACIOS
            print('')

            # ---POR CADA CARACTER AGREGAMOS CIERTO PESO---
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

            # ---EN CASO DE QUE SE INGRESE ALGO DIFERENTE---
            else:
                print('El dato ingresado es invalido, intente nuevamente')
            
            
# ---CREAMOS UNA CLASE QUE SE VA A ENCARGAR DE TODO LO REFERENTE AL TABLERO---
class Tablero(Ingreso_De_Datos):

    # ---INICIALIZAMOS EL TABLERO EN SI---
    def __init__(self):

        # ---LLAMAMOS AL CONTRUCTOR DE LA CLASE PADRE---
        super().__init__()

        # ---LLAMAMOS A LA FUNCION QUE DETERMINARA EL TAMANO DEL TABLERO---
        self.ingreso_dimensiones_tablero()
        
        # ---INICIALIZAMOS UN ARREGLO BIDIMENSIONAL DE NUMPY---
        tablero = np.ones((self.filas, self.columnas), dtype = int)
        self.tablero = tablero
        self.coordenada_x = None 
        self.coordenada_y = None

    def imprimir_tablero(self):
        os.system('cls')
        for i in range(self.filas):
            caracteres = []
            for j in range(self.columnas):
                if self.tablero[i,j] == 1:
                    caracteres.append('.')
                elif self.tablero[i,j] == 3:
                    caracteres.append('H')
                elif self.tablero[i,j] == 7:
                    caracteres.append('~')
                elif self.tablero[i,j] == 9:
                    caracteres.append('X')

            print(*caracteres)

    def colocar_obstaculos(self):

        while True:
            modo = input('a para agregar, s para salir: ')
            if modo == 'a':
                self.ingreso_coordenadas(self.tablero)
                self.tipo_de_obstaculo()
                self.tablero[self.coordenada_x, self.coordenada_y] = self.peso
                self.imprimir_tablero()

            else:
                print("Ingrese coordenadas del punto de incio.")
                self.ingreso_coordenadas(self.tablero)
                self.inicio = (self.coordenada_x, self.coordenada_y)

                print("Ingrese coordenadas del punto de fin.")
                self.ingreso_coordenadas(self.tablero)
                self.fin = (self.coordenada_x, self.coordenada_y)
                

                self.a_estrella()
                break
    def coordenadas_disponibles(self, coordenada):
        lista_de_direcciones = [(1,0),(0,1),(-1,0),(0,-1)]
        lista_de_direcciones_disponibles = []

        for direccion_x, direccion_y in lista_de_direcciones:
            nueva_x = direccion_x + coordenada[0]
            nueva_y = direccion_y + coordenada[1]
            if nueva_x >= 0 and nueva_x < self.filas:
               if nueva_y >= 0 and nueva_y < self.columnas: 
                   if self.tablero[nueva_x, nueva_y] != 9:
                       lista_de_direcciones_disponibles.append((nueva_x,nueva_y))

        return lista_de_direcciones_disponibles
    
    #IMPORTAMOS LAS LIBRERIAS NECESARIAS
import numpy as np
import tkinter as tk
import os
import heapq


#---CREAMOS UNA CLASE PARA QUE SE INGRESEN DISTINTOS TIPOS DE DATOS---
class Ingreso_De_Datos:

    #---PARA INICIALIZAR EL TABLERO CON SU TAMANO---
    def ingreso_dimensiones_tablero(self):

        # ---PEDIMOS FILAS Y COLUMNAS---
        self.filas = int(input("Ingrese el numero de filas del tablero: "))
        self.columnas = int(input("Ingrese el numero de columnas del tablero: "))

    #---PARA COLOCAR DIVERSAS COSAS EN ALGUNA COORDENADA---
    def ingreso_coordenadas(self, tablero):

        # --- USAMOS EL WHILE PARA VERIFICAR QUE LOS DATOS INGRESADOS SEAN VALIDOS---
        while True:

            # ---PEDIMOS LAS COORDENADAS POR SEPARADO---
            coordenada_x = int(input("Ingrese coordenada en x: "))
            coordenada_y = int(input("Ingrese coordenada en y: "))

            # ---VERIFICAMOS QUE NO SE SALGA DEL MAPA---
            if coordenada_x >= 0 and coordenada_x < self.filas and coordenada_y >= 0 and coordenada_y <self.columnas:
                    
                    # ---SI TODO ES VALIDO, INSTANCIAMOS LAS VARIABLES---
                    self.coordenada_x = coordenada_x
                    self.coordenada_y = coordenada_y

                    # ---SALIMOS DEL WHILE---
                    break

            else:

                # ---SI LAS COORDENADAS SON INVALIDAS, CONTINUAMOS PIDIENDO---
                print('Coordenadas se salen del mapa, ingrese nuevamente.')

    # ---EN BASE A ESTO SE CARGARA CIERTO PESO EN LA COORDENADA DE LA CELDA DEL TABLERO---
    def tipo_de_obstaculo(self):

        # ---VOLVEMOS A USAR EL WHILE PARA VERIFICAR LA VALIDEZ DE LOS DATOS---
        while True:

            # ---HACEMOS UN INPUT PIDIENDO EL TIPO DE OBSTACULO---
            tipo = input(
            '---SELECCIONE EL TIPO DE OBSTACULO---' \
            '"c" para camino' \
            '"t" para tierra' \
            '"a" para agua' \
            '"m" para montaña: '
            ).lower().strip() # ---HACEMOS ESTO PARA CONVERTIR A MINUSCULA Y BORRAR LOS ESPACIOS
            print('')

            # ---POR CADA CARACTER AGREGAMOS CIERTO PESO---
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

            # ---EN CASO DE QUE SE INGRESE ALGO DIFERENTE---
            else:
                print('El dato ingresado es invalido, intente nuevamente')
            
            
# ---CREAMOS UNA CLASE QUE SE VA A ENCARGAR DE TODO LO REFERENTE AL TABLERO---
class Tablero(Ingreso_De_Datos):

    # ---INICIALIZAMOS EL TABLERO EN SI---
    def __init__(self):

        # ---LLAMAMOS AL CONTRUCTOR DE LA CLASE PADRE---
        super().__init__()

        # ---LLAMAMOS A LA FUNCION QUE DETERMINARA EL TAMANO DEL TABLERO---
        self.ingreso_dimensiones_tablero()
        
        # ---INICIALIZAMOS UN ARREGLO BIDIMENSIONAL DE NUMPY---
        tablero = np.ones((self.filas, self.columnas), dtype = int)
        self.tablero = tablero
        self.coordenada_x = None 
        self.coordenada_y = None

    def imprimir_tablero(self):
        os.system('cls')
        for i in range(self.filas):
            caracteres = []
            for j in range(self.columnas):
                if self.tablero[i,j] == 1:
                    caracteres.append('.')
                elif self.tablero[i,j] == 3:
                    caracteres.append('H')
                elif self.tablero[i,j] == 7:
                    caracteres.append('~')
                elif self.tablero[i,j] == 9:
                    caracteres.append('X')

            print(*caracteres)

    def colocar_obstaculos(self):

        while True:
            modo = input('a para agregar, s para salir: ')
            if modo == 'a':
                self.ingreso_coordenadas(self.tablero)
                self.tipo_de_obstaculo()
                self.tablero[self.coordenada_x, self.coordenada_y] = self.peso
                self.imprimir_tablero()

            else:
                print("Ingrese coordenadas del punto de incio.")
                self.ingreso_coordenadas(self.tablero)
                self.inicio = (self.coordenada_x, self.coordenada_y)

                print("Ingrese coordenadas del punto de fin.")
                self.ingreso_coordenadas(self.tablero)
                self.fin = (self.coordenada_x, self.coordenada_y)
                

                self.a_estrella()
                break
    def coordenadas_disponibles(self, coordenada):
        lista_de_direcciones = [(1,0),(0,1),(-1,0),(0,-1)]
        lista_de_direcciones_disponibles = []

        for direccion_x, direccion_y in lista_de_direcciones:
            nueva_x = direccion_x + coordenada[0]
            nueva_y = direccion_y + coordenada[1]
            if nueva_x >= 0 and nueva_x < self.filas:
               if nueva_y >= 0 and nueva_y < self.columnas: 
                   if self.tablero[nueva_x, nueva_y] != 9:
                       lista_de_direcciones_disponibles.append((nueva_x,nueva_y))

        return lista_de_direcciones_disponibles
    
    def heuristica(self, coordenada):
        distancia = abs(coordenada[0]-self.fin[0])+abs(coordenada[1]-self.fin[1])
        return distancia
    
    def a_estrella(self):
        cola_prioridad = []
        heuristica_inicio = self.heuristica(self.inicio)
        heapq.heappush(cola_prioridad,(heuristica_inicio,self.inicio))

        diccionario_costos = {self.inicio: 0}
        diccionario_padres = {}
        visitados = set()
        while cola_prioridad:
            _, celda_actual = heapq.heappop(cola_prioridad)

            x,y = celda_actual
            if celda_actual == self.fin:
                self.reconstruir_camino(diccionario_padres)
                return
            visitados.add(celda_actual)
            for vecino in self.coordenadas_disponibles(celda_actual):
                if vecino in visitados:
                    continue
                costo_actual = diccionario_costos[celda_actual]

                costo_vecino = self.tablero[vecino[0],vecino[1]]

                costo_nuevo = costo_actual + costo_vecino

                if vecino not in diccionario_costos or costo_nuevo < diccionario_costos[vecino]:
                    diccionario_costos[vecino] = costo_nuevo

                    diccionario_padres[vecino] = celda_actual

                    prioridad = costo_nuevo + self.heuristica(vecino)

                    heapq.heappush(cola_prioridad,(prioridad,vecino))
        return None
    def reconstruir_camino(self, diccionario_padres):
        camino = []

        actual = self.fin

        while actual != self.inicio:
            camino.append(actual)
            actual = diccionario_padres[actual]
        camino.append(self.inicio)

        camino.reverse()

        print(camino)






            
        







tablero = Tablero()

tablero.colocar_obstaculos()

tablero.imprimir_tablero()


class Buscador_De_Ruta(Tablero, Ingreso_De_Datos):





            
        







tablero = Tablero()

tablero.colocar_obstaculos()

tablero.imprimir_tablero()
