# PAQUETES
# turtle para manejar la interfaz gráfica

from turtle import *
# time Para retrasar el movimiento de la cabeza de la culebra
import time
import random
from tkinter import *
from tkinter import ttk

from bisect import bisect,bisect_left


def mostrar_mensaje(msg, titulo, cuerpo=None):#NO hay eficiencia
  root = Tk()
  root.title(titulo)

  frm = ttk.Frame(root, padding=10)
  frm.grid()
  ttk.Label(frm, text= msg, font=("Arial", 21)).grid(column=0, row=0)
  if cuerpo != None:
    ttk.Label(frm, text= cuerpo, font=("Arial", 18)).grid(column=0, row=1)
  ttk.Button(frm, text="Cerrar", command=root.destroy).grid(column=1, row=0)
  root.mainloop()


mostrar_mensaje("Desplazamiento de la serpiente:", "Instrucciones", "Teclas W S A D / w s a d / 🡡 🡣 🡠 🡢")


# CARACTERÍSTICAS JUEGO
# Cantidad de segundos en que se actualiza el juego
posponer = 0.1

# Tamaño por defecto de la cuadrícula
original = 22
# Factor de aumento del tamaño de la cuadricula
factor = 2
# Tamaño de cuadrícula
cuadricula = original*factor
############################################
malla=[]#lista con lo 13x13 valores
#########################################
# VENTANA
# Inicio
ventana = Screen()

# Configuración
ventana.title("Snake")
ventana.bgcolor("white")
tamano_ventana = (cuadricula*13)+26
ventana.setup(width=tamano_ventana, height=tamano_ventana)
ventana.tracer(0)  # Movimientos más fluidos


# Creación de la grilla 13x13 del juego
for i in range(-6,7):#O(N^2)
    for j in range (-6,7):
        # Creación
        grilla = Turtle()
        # Características
        grilla.speed(0)
        grilla.shape("square")
        grilla.color("gray")
        grilla.penup()  # Para que el turtle no deje rastros al moverse
        grilla.shapesize(stretch_wid=factor, stretch_len=factor,outline=0)

        #añade
        malla.append([cuadricula*i,cuadricula*j])
        # Condiciones iniciales
        grilla.goto(cuadricula*i, cuadricula*j)

        grilla.direction = "stop"

# ***COMIDA***
# Creación
comida = Turtle()
# Características
comida.speed(0)
comida.shape("square")
comida.color("red")
comida.penup()  # Para que el turtle no deje rastros al moverse
comida.shapesize(stretch_wid=factor, stretch_len=factor, outline=0)
# Condiciones iniciales
comida.goto(cuadricula*3, cuadricula*3)
comida.direction = "stop"


# ***CABEZA DE SERPIENTE***
# Creación
cabeza = Turtle()
# Características
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("green")
cabeza.penup()  # Para que el turtle no deje rastros al moverse
cabeza.shapesize(stretch_wid=factor, stretch_len=factor, outline=0)
# Condiciones iniciales
cabeza.goto(0, 0)
cabeza.direction = "stop"




# ***COLAS***
colas = []

# Función creación de la cola inicial
def crear_cola_inicial(): # O(1)
    for i in range(1, 3):
        cola_inicial = Turtle()
        cola_inicial.speed(0)
        cola_inicial.shape("square")
        cola_inicial.color("light green")
        cola_inicial.penup()
        cola_inicial.shapesize(stretch_wid=factor, stretch_len=factor, outline=0)
        cola_inicial.goto(0, -1*cuadricula*i)
        cola_inicial.direction = "stop"
        colas.append(cola_inicial)

# Crear la cola inicial (2 cuerpos)
crear_cola_inicial()

# FUNCIONES
def arriba() -> None:
    """
    Establece la dirección de la cabeza hacia arriba.
    """
    if cabeza.direction != "down":
        # Condicional para que no vaya desde abajo hacia arriba
        cabeza.direction = "up"

def abajo() -> None:
    """
    Establece la dirección de la cabeza hacia abajo.
    """
    if cabeza.direction != "up":
        # Condicional para que no vaya desde la arriba hacia abajo
        cabeza.direction = "down"


def derecha() -> None:
    """
    Establece la dirección de la cabeza hacia la derecha.
    """
    if cabeza.direction != "left":
        # Condicional para que no vaya desde la izquierda hacia la derecha
        cabeza.direction = "right"
    
    global inicio_movimiento
    inicio_movimiento = True

def izquierda() -> None:
    """
    Establece la dirección de la cabeza hacia la izquierda.
    """
    if cabeza.direction != "right":
        # Condicional para que no vaya desde la derecha hacia la izquierda
        cabeza.direction = "left"

def mov() -> None:
    """
    Ejecuta el movimiento de la cabeza de la serpiente según la dirección establecida de la cabeza.
    La librería "turtle" usa una flecha que se mueve manejando la dirección hacia la cual apunta.
    Es por eso que se puede establecer la dirección de la cabeza de la culebra.
    :return: None
    """
    # Se obtiene la posición inicial de la cabeza de la serpiente
    y = cabeza.ycor()
    x = cabeza.xcor()

    if cabeza.direction == "up":
        cabeza.sety(y + cuadricula)

    elif cabeza.direction == "down":
        cabeza.sety(y - cuadricula)

    elif cabeza.direction == "right":
        cabeza.setx(x + cuadricula)

    elif cabeza.direction == "left":
        cabeza.setx(x - cuadricula)


# ***EVENTOS DEL TECLADO***
ventana.listen()
ventana.onkeypress(arriba, "Up")
ventana.onkeypress(abajo, "Down")
ventana.onkeypress(derecha, "Right")
ventana.onkeypress(izquierda, "Left")

ventana.onkeypress(arriba, "W")
ventana.onkeypress(abajo, "S")
ventana.onkeypress(derecha, "D")
ventana.onkeypress(izquierda, "A")

ventana.onkeypress(arriba, "w")
ventana.onkeypress(abajo, "s")
ventana.onkeypress(derecha, "d")
ventana.onkeypress(izquierda, "a")


# Main
while True: #O(k)
    ventana.update()
    colas2=[]#lista con las coordenadas de las colas, se reinician
    #O(1)
    lista12=[]#lista con todas las 13x13 coordenadas menos las que esten en la cola, se reinician
    #O(1)

    # Manejo de la colisión con la comida - crecimiento
    if cabeza.distance(comida) < cuadricula:

        for m in colas:#O(N)
            #añade todas las coordenadas de la cola
            colas2.append([m.xcor(),m.ycor()])

        #añado para que no pueda aparecer en la cabeza
        colas2.append([cabeza.xcor(),cabeza.ycor()])
        #de ordena
        colas2.sort()#2*Nlog(N)

        for cuadrado in range(len(malla)):#N(
            der=bisect(colas2,malla[cuadrado])#2*log(N)+
            izq=bisect_left(colas2,malla[cuadrado])#2*log(N)
            if abs(der-izq)==0:
                lista12.append(malla[cuadrado])#1
                #)
                #=N*log(N)

        #crea un valor random entre 0 y el numero de las colas
        rando=random.randint(0,len(lista12)-1)

        #devuelve alguna de esa lista
        x_cor,y_cor=lista12[rando]

        comida.goto(x_cor,y_cor)

        # Configuración de la cola de la serpiente. Se agrega un cuerpo cada vez
        cola = Turtle()
        cola.speed(0)
        cola.shape("square")
        cola.color("light green")
        cola.penup()
        cola.shapesize(stretch_wid=factor, stretch_len=factor, outline=0)
        colas.append(cola)
        # Disminuir el retardo de renderización
        #posponer -= 0.001
    
    # Chequear si la colisión se da con los bordes de la ventana
    # O(1)
    if cabeza.xcor()>((tamano_ventana/2)-11) or cabeza.xcor()< -((tamano_ventana/2)-11) or cabeza.ycor()> ((tamano_ventana/2)-11) or cabeza.ycor()<- ((tamano_ventana/2)-11):
        cabeza.goto(1000,1000)#cabeza se desaparece
        ventana.update()
        time.sleep(0.3)
        bye()
        mostrar_mensaje("¡Perdiste!", "Notificación")

    # Gestión de la colisión de la cabeza con el cuerpo
    for c in colas: # O(n)
        if c.distance(cabeza) < cuadricula:
            cabeza.goto(1000,1000)#cabeza se desaparece
            ventana.update()
            time.sleep(0.3)
            bye()
            mostrar_mensaje("Perdiste!", "Notificación")
        

    if cabeza.direction != "stop":
        for c in range(len(colas) -1, 0, -1): # O(n)
            x = colas[c - 1].xcor()
            y = colas[c - 1].ycor()
            colas[c].goto(x, y)

        # Mover la posición 0 de la serpiente con la cabeza
        if len(colas) > 0:
            x = cabeza.xcor()
            y = cabeza.ycor()
            colas[0].goto(x, y)

    # Gestión del movimiento de la serpiente
    mov()
    time.sleep(posponer)

ventana.mainloop()
