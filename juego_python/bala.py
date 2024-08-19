import pygame

class Bala:  # Esta va a ser la clase que dara forma a la bala del juego
    def __init__(self, x, y):  # Esta funcion va a recibir un self (como todos los __init__), va a recibir tambien una "x" y una "y"
        self.x = x  # Entonces vamos a decir que su posicion "x" va a ser igual a "x"
        self.y = y
        self.ancho = 15  # Aqui le pondremos el tamaño que tendra nuestra bala
        self.alto = 15
        self.velocidad = 10  # La velocidad a la que se movera la bala - Al cambiar los FPS, si es necesario, tenemos que cambiar la velocidad
        self.color = "white"  # El color que tendra la bala
        self.rect = pygame.Rect(self.x, self.y,  # "rect", es la forma que tiene pygame de crear objetos y definir sus dimensiones, coords ...
                                self.ancho, self.alto)
        self.imagen = pygame.image.load("images/bala.png")
        self.imagen = pygame.transform.scale(self.imagen,(self.ancho, self.alto))


    def dibujar(self, ventana):  # Lo que va a hacer esta funcion es que va a dibujar nuestro rectangulo - (Ventana, se refiere al cod "pygame1.py")
        self.rect = pygame.Rect(self.x, self.y,  # Esta linea tambien deberiamos llamarla en la funcion dibujar, para que se el personaje se mueva sin problemas
                                self.ancho, self.alto)
        ventana.blit(self.imagen, (self.x, self.y))

    def movimiento(self):  # Lo que hara esta funcion, sera mover la bala de abajo hacia arriba
        self.y -= self.velocidad
