import pygame

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

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
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
            self.y -= self.VELOCITY
        else:
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


class GameStats:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


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


    def draw(self):
        self.win.fill(BLACK)

        left_score_text = SCORE_FONT.render(f"{self.left_score}", True, WHITE)
        right_score_text = SCORE_FONT.render(f"{self.right_score}", True, WHITE)

        self.win.blit(left_score_text, (WIDTH * (1/4) - left_score_text.get_width() // 2, 20))
        self.win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

        self.left_paddle.draw(self.win)
        self.right_paddle.draw(self.win)
        self.ball.draw(self.win)

        for i in range(10, HEIGHT, HEIGHT // 20):
            if i % 2 == 1:
                continue
            else:
                pygame.draw.rect(self.win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

        self.ball.draw(self.win)

        pygame.display.update()


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

        stats = GameStats(self.left_hits, self.right_hits, self.left_score, self.right_score)
        return stats

    def paddle_movement(self, pressed_keys):
        if pressed_keys[pygame.K_w] and self.left_paddle.y - self.left_paddle.VELOCITY >= 0:
            self.left_paddle.move(up=True)
        if pressed_keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.VELOCITY + self.left_paddle.height <= HEIGHT:
            self.left_paddle.move(up=False)

        if pressed_keys[pygame.K_UP] and self.right_paddle.y - self.right_paddle.VELOCITY >= 0:
            self.right_paddle.move(up=True)
        if pressed_keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.VELOCITY + self.right_paddle.height <= HEIGHT:
            self.right_paddle.move(up=False)


# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# run = True
# clock = pygame.time.Clock()
# game = Game(WIN)
# while run:
#     game.main_game()
#     clock.tick(FPS)
#
#     pressed_keys = pygame.key.get_pressed()
#
#     if pressed_keys[pygame.K_w]:
#         game.paddle_controls(True)
#     if pressed_keys[pygame.K_s]:
#         game.paddle_controls(False)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#             break

