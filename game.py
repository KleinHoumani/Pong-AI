import pygame

pygame.init()

WIDTH = 700
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
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
    COLOR = WHITE
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
    COLOR = WHITE

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


def draw(win, left_paddle, right_paddle, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", True, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, WHITE)

    win.blit(left_score_text, (WIDTH * (1/4) - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

    left_paddle.draw(win)
    right_paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        else:
            pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_velocity *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.BALL_VELOCITY
                y_velocity = difference_y / reduction_factor
                ball.y_velocity = y_velocity * -1

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.BALL_VELOCITY
                y_velocity = difference_y / reduction_factor
                ball.y_velocity = y_velocity * -1



def handle_paddle_movement(pressed_keys, left_paddle, right_paddle):
    if pressed_keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if pressed_keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if pressed_keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if pressed_keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, left_paddle, right_paddle, ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        pressed_keys = pygame.key.get_pressed()
        handle_paddle_movement(pressed_keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            ball.reset()
            left_score += 1

        if left_score >= WINNING_SCORE:
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

            winner_text = "Left player won!"
            display_winner = SCORE_FONT.render(winner_text, True, WHITE)
            WIN.blit(display_winner, (WIDTH // 2 - display_winner.get_width() // 2, HEIGHT // 2 - display_winner.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            left_score = 0
            right_score = 0

        elif right_score >= WINNING_SCORE:
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

            winner_text = "Right player won!"
            display_winner = SCORE_FONT.render(winner_text, True, WHITE)
            WIN.blit(display_winner, (WIDTH // 2 - display_winner.get_width() // 2, HEIGHT // 2 - display_winner.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__':
    main()
