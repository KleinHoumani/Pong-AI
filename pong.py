import pygame
import random

pygame.init()
WIDTH = 700
HEIGHT = 500
pygame.display.set_caption('Pong')

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("Mecanorma's Blippo Bold", 50)
WINNING_SCORE = 5


class Paddle:
    COLOR = (255, 255, 255)
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            if self.y - self.VELOCITY >= 0:
                self.y -= self.VELOCITY
        elif self.y + self.VELOCITY + self.height <= HEIGHT:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    BALL_VELOCITY = 5
    COLOR = (255, 255, 255)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.BALL_VELOCITY
        self.y_velocity = 0
        # self.y_velocity = random.choice([-4, -3, -2, -1, 1, 2, 3, 4]) # Use this for training

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity *= -1
        self.y_velocity = 0
        # self.y_velocity = random.choice([-4, -3, -2, -1, 1, 2, 3, 4]) #Use this for training


class GameStats:
    def __init__(self, left_hits, right_hits, left_score, right_score, game_over):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score
        self.game_over = game_over


class Game:
    def __init__(self, win):
        self.win = win
        self.left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
        self.left_hits = 0
        self.right_hits = 0
        self.left_score = 0
        self.right_score = 0
        self.winning_score = 5

    def draw(self):
        self.win.fill(BLACK)

        left_score_text = SCORE_FONT.render(f"{self.left_score}", True, WHITE)
        right_score_text = SCORE_FONT.render(f"{self.right_score}", True, WHITE)

        self.win.blit(left_score_text, (WIDTH * (1/4) - left_score_text.get_width() // 2, 20))
        self.win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

        self.left_paddle.draw(self.win)
        self.right_paddle.draw(self.win)
        self.ball.draw(self.win)

        middle_width = 6
        for i in range(10, HEIGHT, HEIGHT // 20):
            if i % 2 == 1:
                continue
            else:
                pygame.draw.rect(self.win, WHITE, (WIDTH // 2 - middle_width // 2, i, middle_width, HEIGHT // 20))

        self.ball.draw(self.win)

        pygame.display.update()

    def menu(self):
        self.win.fill(BLACK)

        easy_text = SCORE_FONT.render("Easy", True, WHITE)
        medium_text = SCORE_FONT.render("Medium", True, WHITE)
        hard_text = SCORE_FONT.render("Hard", True, WHITE)

        rect_width = 200
        rect_height = 70
        rect_x = WIDTH // 2 - rect_width // 2

        pygame.draw.rect(self.win, WHITE, (rect_x, 2 * HEIGHT // 10, rect_width, rect_height), 2)
        pygame.draw.rect(self.win, WHITE, (rect_x, 4 * HEIGHT // 10, rect_width, rect_height), 2)
        pygame.draw.rect(self.win, WHITE, (rect_x, 6 * HEIGHT // 10, rect_width, rect_height), 2)

        self.win.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 2 * HEIGHT // 10 + rect_height // 2 - easy_text.get_height() // 2))
        self.win.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 4 * HEIGHT // 10 + rect_height // 2 - medium_text.get_height() // 2))
        self.win.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 6 * HEIGHT // 10 + rect_height // 2 - hard_text.get_height() // 2))

        option = 0
        mouse_down = pygame.mouse.get_pressed()[0]
        if mouse_down:
            x, y = pygame.mouse.get_pos()
            if x >= rect_x and x <= rect_x + rect_width:
                if y >= 2 * HEIGHT // 10 and y <= 2 * HEIGHT // 10 + rect_height:
                    option += 1
                elif y >= 2 * HEIGHT // 10 and y <= 4 * HEIGHT // 10 + rect_height:
                    option += 2
                elif y >= 2 * HEIGHT // 10 and y <= 6 * HEIGHT // 10 + rect_height:
                    option += 3

        pygame.display.update()
        return option

    def handle_collision(self):
        if self.ball.y + self.ball.radius >= HEIGHT:
            self.ball.y_velocity *= -1
        elif self.ball.y - self.ball.radius <= 0:
            self.ball.y_velocity *= -1

        if self.ball.x_velocity < 0:
            if self.ball.y >= self.left_paddle.y and self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                if self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
                    self.ball.x_velocity *= -1
                    self.left_hits += 1

                    middle_y = self.left_paddle.y + self.left_paddle.height / 2
                    difference_y = middle_y - self.ball.y
                    reduction_factor = (self.left_paddle.height / 2) / self.ball.BALL_VELOCITY
                    y_velocity = difference_y / reduction_factor
                    self.ball.y_velocity = y_velocity * -1

        else:
            if self.ball.y >= self.right_paddle.y and self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                if self.ball.x + self.ball.radius >= self.right_paddle.x:
                    self.ball.x_velocity *= -1
                    self.right_hits += 1

                    middle_y = self.right_paddle.y + self.right_paddle.height / 2
                    difference_y = middle_y - self.ball.y
                    reduction_factor = (self.right_paddle.height / 2) / self.ball.BALL_VELOCITY
                    y_velocity = difference_y / reduction_factor
                    self.ball.y_velocity = y_velocity * -1

    def paddle_controls(self, up):
        if up:
            self.left_paddle.move(True)
        else:
            self.left_paddle.move(False)

    def main_game(self):
        self.draw()
        self.ball.move()
        self.handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > WIDTH:
            self.ball.reset()
            self.left_score += 1

        game_over = False
        if self.left_score >= self.winning_score:
            winner_text = "You win!"
            display_winner = SCORE_FONT.render(winner_text, True, WHITE)
            self.win.blit(display_winner, (WIDTH // 2 - display_winner.get_width() // 2, HEIGHT // 2 - display_winner.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            game_over = True
            self.left_score = 0
            self.right_score = 0

        elif self.right_score >= self.winning_score:
            winner_text = "AI wins!"
            display_winner = SCORE_FONT.render(winner_text, True, WHITE)
            self.win.blit(display_winner, (WIDTH // 2 - display_winner.get_width() // 2, HEIGHT // 2 - display_winner.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            game_over = True
            self.left_score = 0
            self.right_score = 0

        stats = GameStats(self.left_hits, self.right_hits, self.left_score, self.right_score, game_over)

        return stats
