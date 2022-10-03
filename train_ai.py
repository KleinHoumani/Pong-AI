import os
import neat
import pygame
from pong import Game
import time
import pickle


class PongAI:
    def __init__(self, win):
        self.game = Game(win)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball


    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        start_time = time.time()

        while run:
            output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            move1 = output1.index(max(output1))

            output2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            move2 = output2.index(max(output2))

            if move1 == 0:
                genome1.fitness -= 0.01
            if move1 == 1:
                self.left_paddle.move(True)
            if move1 == 2:
                self.left_paddle.move(False)

            if move2 == 0:
                genome2.fitness -= 0.01
            if move2 == 1:
                self.right_paddle.move(True)
            if move2 == 2:
                self.right_paddle.move(False)

            stats = self.game.main_game()
            duration = time.time() - start_time

            if stats.left_score > 0 or stats.right_score > 0 or stats.left_hits > 30:
                self.determine_fitness(genome1, genome2, stats)
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

    def set_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_w]:
                self.left_paddle.move(True)
            if pressed_keys[pygame.K_s]:
                self.left_paddle.move(False)

            output = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            move = output.index(max(output))

            if move == 0:
                pass
            if move == 1:
                self.right_paddle.move(True)
            if move == 2:
                self.right_paddle.move(False)


            stats = self.game.main_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()


    def determine_fitness(self, genome1, genome2, stats):
        genome1.fitness += stats.left_hits
        genome2.fitness += stats.right_hits


def eval_genomes(genomes, config):
    width = 700
    height = 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Training")

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0

        genome_id2, genome2 = genomes[i+1]
        if genome2.fitness is None:
            genome2.fitness = 0

            training = PongAI(win)
            training.train_ai(genome1, genome2, config)


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    # population.add_reporter(neat.StdOutReporter)
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))

    winner = population.run(eval_genomes, 50)

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def play_ai(config):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    width = 700
    height = 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong AI")

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    pong = PongAI(win)
    pong.set_ai(winner, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    # run(config_path)
    play_ai(config_path)
