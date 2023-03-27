import sys
import os
import pygame

from Bird import Bird
from Pipe import Pipe
from Ground import Ground
from Background import BACKGROUD_IMAGE
from AI import AI

AI_PLAYING = True
COLLISION = True

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
COLOR_WHITE = (255, 255, 255)
FRAME_RATE = 30

pygame.display.set_caption("Flappy Bird + AI")

pygame.font.init()
FONT = pygame.font.SysFont('arial', 40)

def draw_screen(screen, birds, pipes, ground, points, generation):
    screen.blit(BACKGROUD_IMAGE, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    ground.draw(screen)

    text = FONT.render(f"Points: {points}", 1, COLOR_WHITE)
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    if AI_PLAYING:
        text = FONT.render(f"Generation: {generation}", 1, COLOR_WHITE)
        screen.blit(text, (10, 10))

        text = FONT.render(f"Population: {len(birds)}", 1, COLOR_WHITE)
        screen.blit(text, (10, 60))
    else:
        if len(birds) == 0:
            text = FONT.render("Game over", 1, COLOR_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text, text_rect)

    pygame.display.update()

def main(genomes, config): # fitness function
    if AI_PLAYING:
        ai.init_genomes(genomes, config)
        ai.inc_generation()

        birds = []  
        for _ in enumerate(ai.genome_list):
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]

    pipes = [Pipe(700)]
    ground = Ground(730)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    points = 0

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FRAME_RATE)

        # player events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if not AI_PLAYING:
                if len(birds) == 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            main(None, None)
                            break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()

        if AI_PLAYING:
            pipe_index = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].TOP_PIPE.get_width()):
                    pipe_index = 1
            else:
                break

        # moving the birds
        for i, bird in enumerate(birds):
            bird.move()
            if AI_PLAYING:
                # increasing the fitness of the bird
                ai.update_fitness(i, 0.1)

                # output
                # The distance between the bird and the ground
                # The distance between the bird and the top pipe
                # The distance between the bird and the base pipe
                output = ai.activate(i, (
                    bird.y, 
                    abs(bird.y - pipes[pipe_index].height), 
                    abs(bird.y - pipes[pipe_index].base_position))) 

                # between -1 and 1. If more than > 0.5, the bird jumps
                if output[0] > 0.5:
                    bird.jump()

        # moving the ground
        ground.move()

        # moving the pipes
        add_pipe = False
        removed_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collision(bird, COLLISION):
                    birds.pop(i)
                    if AI_PLAYING:
                        ai.update_fitness(i, -1)
                        ai.drop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                removed_pipes.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
            if AI_PLAYING:
                for i, _ in enumerate(ai.genome_list):
                    ai.update_fitness(i, 5)

        for pipe in removed_pipes:
            pipes.remove(pipe)

        # when birds fall
        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > ground.y or bird.y < 0:
                birds.pop(i)
                if AI_PLAYING:
                    #genome_list[i].fitness -= 1 # only if it is necessary to penalize the AI when it falls
                    ai.drop(i)

        draw_screen(screen, birds, pipes, ground, points, ai.generation if AI_PLAYING else None)
        pygame.display.flip()

    if not running:
        pygame.quit()
        sys.exit()

if __name__ == '__main__':    
    if AI_PLAYING:
        ai = AI()
        path = os.path.dirname(__file__)
        config_path = os.path.join(path, 'config.txt')
        ai.start(config_path, main, True)
    else:
        main(None, None)
