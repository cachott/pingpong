import tkinter as tk
import random

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Ping Pong")

# Tamaño de la ventana
ancho_ventana = 800
alto_ventana = 600
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

# Colores
color_fondo = "black"
color_raquetas = "white"
color_pelota = "white"

# Raqueta del jugador
jugador_ancho = 15
jugador_alto = 100
jugador = tk.Canvas(ventana, width=jugador_ancho, height=jugador_alto, bg=color_raquetas)
jugador.place(x=50, y=(alto_ventana - jugador_alto) // 2)

# Raqueta del oponente
oponente_ancho = 15
oponente_alto = 100
oponente = tk.Canvas(ventana, width=oponente_ancho, height=oponente_alto, bg=color_raquetas)
oponente.place(x=ancho_ventana - 50 - oponente_ancho, y=(alto_ventana - oponente_alto) // 2)

# Pelota
pelota_diametro = 20
pelota = tk.Canvas(ventana, width=pelota_diametro, height=pelota_diametro, bg=color_pelota)
pelota.place(x=(ancho_ventana - pelota_diametro) // 2, y=(alto_ventana - pelota_diametro) // 2)

# Velocidad de movimiento
velocidad_x = 5
velocidad_y = 5

# Función para mover la raqueta del jugador
def mover_raqueta(event):
    key = event.keysym
    if key == "Up" and jugador.winfo_y() > 0:
        jugador.move(0, -20)
    elif key == "Down" and jugador.winfo_y() < alto_ventana - jugador_alto:
        jugador.move(0, 20)

# Función para mover la pelota
def mover_pelota():
    global velocidad_x, velocidad_y

    pelota_x, pelota_y, _, _ = pelota.coords("all")
    pelota.move(velocidad_x, velocidad_y)

    # Colisiones con las paredes
    if pelota_y <= 0 or pelota_y >= alto_ventana - pelota_diametro:
        velocidad_y *= -1

    # Colisiones con las raquetas
    if pelota_x <= jugador_ancho and jugador.winfo_y() <= pelota_y <= jugador.winfo_y() + jugador_alto:
        velocidad_x *= -1
    elif pelota_x + pelota_diametro >= ancho_ventana - oponente_ancho and oponente.winfo_y() <= pelota_y <= oponente.winfo_y() + oponente_alto:
        velocidad_x *= -1

    # Punto anotado
    if pelota_x < 0:
        reiniciar_partida()
        aumentar_puntuacion(oponente_puntuacion)
    elif pelota_x + pelota_diametro > ancho_ventana:
        reiniciar_partida()
        aumentar_puntuacion(jugador_puntuacion)

    ventana.after(20, mover_pelota)

# Función para reiniciar la partida
def reiniciar_partida():
    pelota.place(x=(ancho_ventana - pelota_diametro) // 2, y=(alto_ventana - pelota_diametro) // 2)
    global velocidad_x, velocidad_y
    velocidad_x = random.choice((5, -5))
    velocidad_y = random.choice((5, -5))

# Función para aumentar la puntuación
def aumentar_puntuacion(label):
    puntuacion = int(label.cget("text"))
    puntuacion += 1
    label.config(text=str(puntuacion))

# Etiquetas para la puntuación
jugador_puntuacion = tk.Label(ventana, text="0", fg=color_raquetas, font=("Helvetica", 24))
jugador_puntuacion.place(x=ancho_ventana // 4, y=20)

oponente_puntuacion = tk.Label(ventana, text="0", fg=color_raquetas, font=("Helvetica", 24))
oponente_puntuacion.place(x=3 * ancho_ventana // 4, y=20)

# Asociar eventos de teclado
ventana.bind("<Up>", mover_raqueta)
ventana.bind("<Down>", mover_raqueta)

# Iniciar el juego
reiniciar_partida()
mover_pelota()

# Iniciar la ventana
ventana.mainloop()
