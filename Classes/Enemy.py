import pygame


# Enemy Class
class Enemy:
    def __init__(self, x, y, width, height, speed, direction, start, end):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.start = start
        self.end = end
        self.rect = pygame.Rect(x, y, width, height)
