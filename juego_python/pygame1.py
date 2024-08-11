import pygame
import random

from personaje import Cubo  #Importamos el codigo de "personaje.py"
from enemigo import Enemigo  #Importamos el codigo de "enemigo.py"


pygame.init()   # Inicializar Pygame

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode ([ANCHO, ALTO])       #.display => Lo usamos para referirnos a todo lo que tiene que ver con la pantalla
FPS = 60    # Para el uso del time.Clock(), tenemos que definir los fps, para que en todos los ordenadores vaya a los mismos FPS

# Para que la pantalla no se cierre automaticamente, tendremos que utilizar un bucle:
# [Bucle principal del juego]

jugando = True

reloj = pygame.time.Clock()     # Tenemos que crear mas enemigos, por ello, vamos a crear un reloj para que ada cierto tiempo se genere un enemigo

vida = 5    # Vamos ha hacer un sistemas de vidas, en el que tendremos una cantidad de vidas
puntos = 0  # Vamos ha hacer un sistemas de puntos

tiempo_pasado = 0   # Tenemos que ver el tiempo que ha pasado de un punto a otro para asi crear nuevos enemigos 
tiempo_entre_enemigos = 500     # Esto va a ser la cantidad de milisegundos que tienen que pasar desde que aparece un enemigos hasta que aparece otro

cubo = Cubo(ANCHO/2, ALTO -80)   # Hemos quitado que el player se mueve de arriba a abajo, entonces tenemos que poner la posicion inicial desde abajo para poder esquivar a los enemigos con facilidad

enemigos = []   # Creamos esta variable, para tener una lista de todos los enemigos que aparezcan en la pantalla, para poder tackear su posicion, su velocidad...
enemigos.append(Enemigo(ANCHO/2, 100))  # Estas coordenadas nos llevaran a la posicion donde aparecera el enemigo

def gestionar_teclas(teclas):    # Lo que va a hacer es comprobar si dentro de nuestas teclas hay un
    """
    if teclas[pygame.K_w] :    # Con esto nos referimos a una tecla especifica
        cubo.y -= cubo.velocidad    # Si pulsamos la "w" queremos que la posicion "y" de nuestro cubo se reste (vaya hacia arriba)
    if teclas[pygame.K_s] :
        cubo.y += cubo.velocidad    # Si pulsamos la "s" queremos que la posicion "y" de nuestro cubo se sume (vaya hacia abajo)
    """
    if teclas[pygame.K_a] :
        cubo.x -= cubo.velocidad    # Si pulsamos la "a" queremos que la posicion "x" de nuestro cubo se reste (vaya hacia la izquieda)
    if teclas[pygame.K_d] :
        cubo.x += cubo.velocidad    # Si pulsamos la "d" queremos que la posicion "x" de nuestro cubo se sume (vaya hacia derecha)


while jugando and vida > 0:   # La funcion principal del bucle es que jugaremos si nuestra vida es superior a 0, es decir, si nuestra vida es 0 no podremos jugar

    tiempo_pasado += reloj.tick(FPS)    # Lo que estamos haciendo es que en tiempo_pasado estan añadiendose todos los milisegundos que pasan
        # print(tiempo_pasado)

    if tiempo_pasado > tiempo_entre_enemigos:   # Si tiempo_pasado es mayor al tiempo_entre_enemigos, 
        enemigos.append(Enemigo(random.randint(0, ANCHO), -50))   # Crearemos un nuevo enemigo en la parte de arriba de manera random
        tiempo_pasado = 0   # Para no crear un bucle infinito, una vez el tiempo_pasado pasa a tiempo_entre_enemigo pues esta creando infinitos enemigos

    eventos = pygame.event.get()        # Esto nos va a devolver una lista con todos lo eventos que hay

    teclas = pygame.key.get_pressed()      # Esto va a contener nuestras teclas pulsadas, esto lo que hace es formar una lista con las teclas que se pulsan
    
    gestionar_teclas(teclas) 

    for evento in eventos:
        if evento.type == pygame.QUIT:      # Esto puede suceder, si nos salimos de la pantalla, pulsamos ALT + F4, apagamos el ordenador
            jugando = False

    VENTANA.fill("black")   # En cada vuelta de nuestro bucle principal, lo que tenemos que haces es llnear nuestra pantalla en el color de fondo, para que este no se dibuje de lineas extrañas

    cubo.dibujar(VENTANA)       # Cada vez que de una vuelta a nuestro bucle principal

    for enemigo in enemigos:    # Vamos a actualizar las posiciones de los enemigos
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()    # Esto lo que hara sera recebir el movimiento del enemigo

        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):    # Esto sirve para ver si nuestro player esta colisionando con un enemigo - .erct, quiere decir que va a hacer el rectangulo de cada personaje individualmente
            print("Tocado") #Si esto da verdadero, tenemos que imprimir "Tocado"
            vida -= 1  #ademas, de quitarnos 1 vida de la cantidad total que tenemos
            print(f"Te quedan {vida} vidas")   # Cada vez que nos quiten 1 vida, lo imprimiremos por pantalla para tener siempre constancia de las que nos quedan
            enemigos.remove(enemigo)    # Y si chocamos contra un enemigo en lugar de sopbrepasarlo, este se eliminara automaticamente cuando nos quite 1 vida


    pygame.display.update()       # Actualiza nuestra pantalla constantemente

pygame.quit()       # Salir de Pygame
