import os
import neat
import pygame
from pong import Game



def train_ai(game, genome1, genome2, config):
    run = True
    while run:
        game.main_game()
        game.draw()
        pygame.display.update()


def eval_genomes(genomes, config):
    width = 700
    height = 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Training")

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1]:
            if genome2.fitness == None:
                genome2.fitness = 0
            else:
                genome2.fitness = genome2.fitness
            game = Game(win)



def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter)
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(1))

    winner = population.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
