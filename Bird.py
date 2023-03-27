import pygame
import os

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

class Bird:
    IMGS = BIRD_IMAGES
    # rotation animations
    MAX_ROTATION = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_count = 0
        self.image = self.IMGS[0]
    
    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y
    
    def move(self):
        # calcule the movement
        self.time += 1
        movement = 1.5 * (self.time**2) + self.speed * self.time

        # restrict movement
        if movement > 16:
            movement = 16
        elif movement < 0:
            movement -= 2

        self.y += movement

        # the angle of the bird
        if movement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED
    
    def draw(self, screen):
        # define which image to use
        self.image_count += 1
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMGS[0]
            self.image_count = 0

        # if the bird is falling, it doesn't flap its wings
        if self.angle >= -80:
            self.image = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME*2

        # draw the image
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center_pos = self.image.get_rect(topleft=(self.x, self.y)).center
        rect = rotated_image.get_rect(center=image_center_pos)
        screen.blit(rotated_image, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
