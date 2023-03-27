import pygame
import os
import random

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))

class Pipe:
    DISTANCE = 200
    SPEED_X = 5
    SPEED_Y = 4
    UP = 0
    DOWN = 1    

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.base_position = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.BASE_PIPE = PIPE_IMAGE
        self.passed = False
        self.direction = random.randrange(0, 2)
        self.set_height(random.randrange(50, 450))

    def set_height(self, value):
        self.height += value
        self.top_position = self.height - self.TOP_PIPE.get_height()
        self.base_position = self.height + self.DISTANCE
    
    def move(self):
        self.x -= self.SPEED_X

        if self.direction == self.UP:
            if self.height > 100:
                self.set_height(self.SPEED_Y * -1)
            else:
                self.direction = self.DOWN  

        if self.direction == self.DOWN:
            if self.height < 400:
                self.set_height(self.SPEED_Y)
            else:
                self.direction = self.UP 

    def draw(self, screen):
        screen.blit(self.TOP_PIPE, (self.x, self.top_position))        
        screen.blit(self.BASE_PIPE, (self.x, self.base_position))

    def collision(self, bird, with_collision):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BASE_PIPE)

        top_distance = (self.x - bird.x, self.top_position - round(bird.y))
        base_distance = (self.x - bird.x, self.base_position - round(bird.y))

        if with_collision:
            has_top_point = bird_mask.overlap(top_mask, top_distance)
            has_base_point = bird_mask.overlap(base_mask, base_distance)
        else:
            has_top_point = False
            has_base_point = False

        return has_top_point or has_base_point        
