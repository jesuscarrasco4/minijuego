import pygame

class Enemigo:     # Esta va a ser la clase que dara forma al enemigo del juego
    def __init__(self, x, y):   # Esta funcion va a recibir un self (como todos los __init__), va a recebir tambien una "x" y una "y"
        self.x = x              # Entonces vamos a decir que su posicion "x" va a ser igual a "x"
        self.y = y
        self.ancho = 50         # Aqui le pondremos el tamaño que tendra nuestro enemigo
        self.alto = 50
        self.velocidad = 5      # La velocidad a la que se movera el enemigo - Al cambiar los FPS, si es necesario, tenemos que cambiar la velocidad
        self.color = "blue"     # El colo que tendra el enemigo
        self.rect = pygame.Rect(self.x, self.y,             # "rect", es la forma que tiene pygame de crear objetos y 
                                self.ancho, self.alto)      # definir sus dimensiones, coords ...
    
    def dibujar(self, ventana):     # Lo que va a hacer esta funcion es que va a dibujar nuestro rectangulo - (Ventana, se refiere al cod "pygame1.py")
        pygame.draw.rect(ventana, self.color, self.rect)
        self.rect = pygame.Rect(self.x, self.y,            # Esta linea tambien deberiamos llamarla en la duncion dibujar, para que 
                                self.ancho, self.alto)     # se el personaje se mueva sin problemas
        
    def movimiento(self):   #Lo que hara esta linea, sera mover el enemigo de una sola manera, de arriba hacia abajo
        self.y += self.velocidad