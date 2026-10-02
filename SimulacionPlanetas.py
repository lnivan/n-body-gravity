import pygame
import math
import random
import time

gameLength = 1400
gameWidth = 800

white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode([gameLength, gameWidth])


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.module = math.sqrt(x**2 + y**2)
    
    def __add__(self, other):
        return(Vector2(self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return(Vector2(self.x - other.x, self.y - other.y))

    def __mul__(self, other):
        return(Vector2(self.x * other, self.y * other))

    def EM(self, other):
        return(self.x * other.x + self.y * other.y)

    def normalize(self):
        return(Vector2(self.x / self.module, self.y / self.module))

    def turn(self, radian):
        newRadian = math.atan2(self.y, self.x) + radian
        self.x = math.cos(newRadian) * self.module
        self.y = math.sin (newRadian) * self.module


class Planet:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.radius = math.sqrt(mass / math.pi)
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector2(0, 0)
        self.lastFrame = time.time()

    def updateAcceleration(self, planets):
        self.acceleration = Vector2(0, 0)
        for otherPlanet in planets:
            if otherPlanet != self:
                self.acceleration = self.acceleration + (otherPlanet.position - self.position).normalize() * ((6.67 * 10 ** (1)) * self.mass * otherPlanet.mass / (otherPlanet.position - self.position).module ** 2) * (1 / self.mass)

    def updatePosition(self, deltaTime, timeScale):
        self.velocity = self.velocity + self.acceleration * deltaTime * timeScale
        self.position = self.position + self.velocity * deltaTime * timeScale

    def draw(self):
        pygame.draw.circle(screen, white, [self.position.x, self.position.y], self.radius, 0)


class PlanetSystem:
    def __init__(self):
        self.planets = []
        self.lastUpdate = time.time()
        self.timeScale = 20
    
    def addPlanet(self, mass, position, velocity):
        self.planets.append(Planet(mass, position, velocity))
    
    def update(self):
        deltaTime = time.time() - self.lastUpdate
        self.lastUpdate = time.time()
        for planet in self.planets:
            planet.updateAcceleration(self.planets)
        for planet in self.planets:
            planet.updatePosition(deltaTime, self.timeScale)

    def draw(self):
        screen.fill(black)
        for planet in self.planets:
            planet.draw()





universe = PlanetSystem()
universe.addPlanet(1000, Vector2(700, 400), Vector2(0, 1.2))
universe.addPlanet(100, Vector2(1000, 400), Vector2(0, -15))
universe.addPlanet(7, Vector2(1050, 400), Vector2(0, -25))

running = True
while running == True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    universe.draw()
    pygame.display.flip()
    universe.update()
