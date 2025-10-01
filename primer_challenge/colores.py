import numpy as np
import tkinter as tk

# --- Variables Globales ---
matriz = np.zeros((10, 10), dtype=int)
botones = []
estado = "inicial"
inicio = None
fin = None

# --- Funciones ---
def cambiar_color(i, j):
    global estado, inicio, fin

    if estado == "inicial":  # solo pintamos en esta fase
        if matriz[i, j] == 0:
            matriz[i, j] = 5
            botones[i][j].config(bg="blue")
        elif matriz[i, j] == 5:
            matriz[i, j] = 9
            botones[i][j].config(bg="black")
        elif matriz[i, j] == 9:
            matriz[i, j] = 0
            botones[i][j].config(bg="white")
        print(matriz)

    elif estado == "seleccionando_inicio":  # ahora elegimos inicio
        inicio = (i, j)
        botones[i][j].config(bg="green")
        label_estado.config(text=f"Inicio: {inicio}. Ahora seleccione el fin.")
        estado = "seleccionando_fin"
        print(f"Inicio seleccionado: {inicio}")

    elif estado == "seleccionando_fin":  # ahora elegimos fin
        fin = (i, j)
        botones[i][j].config(bg="red")
        label_estado.config(text=f"Fin: {fin}. Proceso terminado.")
        estado = "terminado"
        print(f"Fin seleccionado: {fin}")
        print(f"Coordenadas finales: Inicio={inicio}, Fin={fin}")


def mapa_terminado():
    global estado, matriz, inicio, fin

    if estado == "inicial":
        estado = "seleccionando_inicio"
        label_estado.config(text="Seleccione el inicio (celda verde)")
        boton_listo.config(text="Reiniciar")
    else:
        # Reinicio total
        estado = "inicial"
        matriz = np.zeros((10, 10), dtype=int)
        inicio = None
        fin = None
        for i in range(10):
            for j in range(10):
                botones[i][j].config(bg="white")
        label_estado.config(text="Seleccione un punto en el mapa")
        boton_listo.config(text="Listo")


# --- Interfaz Gráfica ---
root = tk.Tk()
root.title("Tablero con matriz numpy")

label_estado = tk.Label(root, text="Seleccione un punto en el mapa")
label_estado.grid(row=0, column=0, columnspan=10)

# Crear el tablero de botones
for i in range(10):
    fila = []
    for j in range(10):
        btn = tk.Button(root, width=3, height=1,
                        bg="white",
                        command=lambda x=i, y=j: cambiar_color(x, y))
        btn.grid(row=i + 1, column=j)  # Fila 0 ya la ocupa el label
        fila.append(btn)
    botones.append(fila)

# Botón de "Listo"
boton_listo = tk.Button(root, text="Listo", command=mapa_terminado)
boton_listo.grid(row=12, column=0, columnspan=10, sticky="nsew", pady=10)

# Iniciar el bucle principal de la aplicación
root.mainloop()
