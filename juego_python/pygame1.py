import pygame
import random

from personaje import Cubo  # Importamos el código de "personaje.py"
from enemigo import Enemigo  # Importamos el código de "enemigo.py"
from item import Item  # Importamos el código de "item.py"
from bala import Bala  # Importamos el código de "bala.py"

pygame.init()  # Inicializar Pygame
pygame.mixer.init()

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO, ALTO])  # Configurar la ventana del juego
FPS = 60  # Definir los frames por segundo
FUENTE = pygame.font.SysFont("Urban", 40)  # Fuente y tamaño para textos en pantalla
SONIDO_DISPARO = pygame.mixer.Sound("audio\disparo.wav")
SONIDO_MUERTE = pygame.mixer.Sound("audio\muerte.wav")

# Cargar y escalar la imagen de fondo
fondo = pygame.image.load("images/fondo.png")  # Ruta de la imagen de fondo
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Escalar la imagen al tamaño de la ventana

jugando = True

reloj = pygame.time.Clock()

vida = 5  # Vidas iniciales del jugador
puntos = 0  # Puntuación inicial del jugador

tiempo_pasado_enemigos = 0  # Tiempo transcurrido desde la aparición del último enemigo
tiempo_entre_enemigos = 500  # Tiempo entre la aparición de enemigos en milisegundos

tiempo_pasado_items = 0  # Tiempo transcurrido desde la aparición del último item
tiempo_entre_items = 10000  # Tiempo entre la aparición de items en milisegundos

cubo = Cubo(ANCHO / 2, ALTO - 80)  # Posición inicial del jugador

enemigos = []  # Lista para almacenar enemigos
enemigos.append(Enemigo(ANCHO / 2, 100))  # Añadir un primer enemigo

items = []  # Lista para almacenar items de vida

balas = []  # Lista para almacenar balas disparadas por el jugador

ultima_bala = 0  # Para controlar el tiempo entre disparos
tiempo_entre_balas = 1  # Tiempo en milisegundos entre cada disparo

def crear_bala():
    global ultima_bala

    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(Bala(cubo.rect.centerx, cubo.rect.centery))  # Crear una nueva bala en la posición del jugador
        ultima_bala = pygame.time.get_ticks()
        SONIDO_DISPARO.play()


def gestionar_teclas(teclas):  # Comprobar el estado de las teclas
    if teclas[pygame.K_a] and cubo.x > 0:  # Limitar el movimiento hacia la izquierda
        cubo.x -= cubo.velocidad
    if teclas[pygame.K_d] and cubo.x < ANCHO - cubo.ancho:  # Limitar el movimiento hacia la derecha
        cubo.x += cubo.velocidad


while jugando and vida > 0:  # Bucle principal del juego

    tiempo_pasado_enemigos += reloj.tick(FPS)  # Incrementar el tiempo pasado en cada ciclo para controlar la aparición de enemigos
    tiempo_pasado_items += reloj.get_time()  # Incrementar el tiempo pasado para controlar la aparición de items

    # Crear un nuevo enemigo si ha pasado el tiempo suficiente
    if tiempo_pasado_enemigos > tiempo_entre_enemigos:
        enemigos.append(Enemigo(random.randint(0, ANCHO), -50))  # Crear un enemigo en una posición aleatoria en la parte superior
        tiempo_pasado_enemigos = 0  # Reiniciar el contador de tiempo para enemigos

    # Crear un nuevo item si ha pasado el tiempo suficiente
    if tiempo_pasado_items > tiempo_entre_items:
        items.append(Item(random.randint(0, ANCHO), -50))  # Crear un item en una posición aleatoria en la parte superior
        tiempo_pasado_items = 0  # Reiniciar el contador de tiempo para items

    eventos = pygame.event.get()  # Obtener todos los eventos del juego

    teclas = pygame.key.get_pressed()  # Obtener las teclas presionadas

    texto_vidas = FUENTE.render(f"Vida: {vida}", True, "White")
    texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, "White")

    gestionar_teclas(teclas)  # Mover el jugador de acuerdo a las teclas presionadas

    for evento in eventos:
        if evento.type == pygame.QUIT:  # Salir del juego si se cierra la ventana
            jugando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:  # Crear una bala si se presiona la barra espaciadora
            crear_bala()

    VENTANA.blit(fondo, (0, 0))  # Dibujar la imagen de fondo

    cubo.dibujar(VENTANA)  # Dibujar al jugador en la pantalla

    # Manejo de enemigos
    for enemigo in enemigos:
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()

        # Colisión del jugador con un enemigo
        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
            print("Tocado")
            vida -= 1  # Quitar una vida al jugador
            enemigos.remove(enemigo)  # Eliminar el enemigo que colisionó

        # Eliminar enemigo si sale de la pantalla
        if enemigo.y > ALTO:
            enemigos.remove(enemigo)

        # Colisión de una bala con un enemigo
        for bala in balas:
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                balas.remove(bala)
                enemigo.vida -= 1

        if enemigo.vida <= 0:
            enemigos.remove(enemigo)
            puntos += 1  # Sumar un punto por cada enemigo eliminado

    # Manejo de items
    for item in items:
        item.dibujar(VENTANA)
        item.movimiento()

        # Colisión del jugador con un item
        if pygame.Rect.colliderect(cubo.rect, item.rect):
            print("¡Vida extra!")
            vida += 1  # Aumentar una vida al jugador
            items.remove(item)  # Eliminar el item que fue recogido

        # Eliminar item si sale de la pantalla
        if item.y > ALTO:
            items.remove(item)

    # Manejo de balas
    for bala in balas:
        bala.movimiento()
        bala.dibujar(VENTANA)
        if bala.y < 0:  # Eliminar las balas que salen de la pantalla
            balas.remove(bala)

    VENTANA.blit(texto_vidas, (20, 20))
    VENTANA.blit(texto_puntos, (20, 70))

    pygame.display.update()  # Actualizar la pantalla

SONIDO_MUERTE.play()

pygame.quit()
nombre = input("Introduce tu nombre: ")

with open("puntuaciones.txt", "a") as archivo:
    archivo.write(f"{nombre} - {puntos}\n")
