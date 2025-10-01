class Tablero:
    
    def __init__(self):
        self.filas = int(input('ingrese el numero de filas: '))
        self.columnas = int(input('ingrese el numero de columnas: '))

    def crear_tablero(self):
        import numpy as np

        filas = self.filas

        columnas = self.columnas
        tablero = np.ones((filas, columnas), dtype=int)

        return tablero
    
    def agregar_obstaculos(self, tablero, coordenadas, valor):

        tablero[coordenadas[0], coordenadas[1]] = valor

        return tablero
    
    def celdas_accesibles(self, tablero, coordenadas):
        direcciones = [(1,0),(0,1),(-1,0),(0,-1)]
        direcciones_disponibles = []

        for direccion_x, direccion_y in direcciones:
            coordenada_x, coordenada_y = coordenadas
            posicion_x = coordenada_x + direccion_x
            posicion_y = coordenada_y + direccion_y
            if 0 <= posicion_x < self.filas and 0 <= posicion_y < self.columnas and tablero[posicion_x,posicion_y] != 9:
                coordenada = (posicion_x,posicion_y)
                direcciones_disponibles.append(coordenada)

        print(direcciones_disponibles)




        
    



objeto_tablero = Tablero()

objeto_tablero.__init__

tablero = objeto_tablero.crear_tablero()

objeto_tablero.celdas_accesibles(tablero, (1,1))

print(tablero)






