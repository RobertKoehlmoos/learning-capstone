# Lets you play Pong!
# left player uses the W and S keys to move up and down
# right player uses the up and down arrow keys to move up and down
import pygame
import random
import math

# define some colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)

# basic constants to set up your game
WIDTH = 800
HEIGHT = 480
FPS = 30
BGCOLOR = BLACK
OBJECT_COLOR = WHITE
PLAY_WIDTH = (50, 750)
PLAY_HEIGHT = (40, 440)
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7  # lucky number seven
BALL_INIT_SPEED = 11.0  # choosen through trial and error

# initialize pygame
pygame.init()
# initialize sound - uncomment if you're using sound
# pygame.mixer.init()
# create the game window and set the title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
# start the clock
clock = pygame.time.Clock()
# setting the font
font = pygame.font.SysFont('consolas', 32)


# Setting up classes and objects
class Paddle:  # will be the left and right paddles
    def __init__(self, x: int, width: int, height: int):
        self.x = x  # location of the right edge of the paddle
        self.y = (PLAY_HEIGHT[0] + PLAY_HEIGHT[1])//2  # paddle starts in the middle
        self.width = width  # width of the paddle
        self.height = height  # height of the paddle

    def move_up(self):
        if self.y - PADDLE_HEIGHT//2 - PADDLE_SPEED > PLAY_HEIGHT[0]:  # making sure we don't go above the top
            self.y -= PADDLE_SPEED

    def move_down(self):
        if self.y + PADDLE_HEIGHT//2 + PADDLE_SPEED < PLAY_HEIGHT[1]:  # making sure we don't go below the bottom
            self.y += PADDLE_SPEED

    def get_rect(self) -> pygame.Rect:  # returns the pygame rectangle to draw the paddle
        return pygame.Rect(self.x - self.width, self.y - self.height // 2, self.width, self.height)


class Ball:
    def __init__(self, x: int, y: int, radius: float):
        self.x = x  # starting location
        self.y = y  # starting location
        self.radius = radius  # for drawing the ball
        self.y_speed = 0.0
        self.x_speed = 0.0
        self.random_initial_speed()

    def random_initial_speed(self):  # sets the ball in a slow but random direction
        init_angle = 2 * math.pi * random.random()
        self.x_speed = BALL_INIT_SPEED * math.cos(init_angle)
        self.y_speed = BALL_INIT_SPEED * math.sin(init_angle)
        if abs(self.x_speed) < 5:  # making sure the ball doesn't start off just going up and down
            self.x_speed = 5 if self.x_speed > 0 else -5

    def reset(self, x, y):  # resets the ball for a new round
        self.x = x
        self.y = y
        self.random_initial_speed()


left_paddle = Paddle(PLAY_WIDTH[0], PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = Paddle(PLAY_WIDTH[1], PADDLE_WIDTH, PADDLE_HEIGHT)

ball = Ball(sum(PLAY_WIDTH)//2, sum(PLAY_HEIGHT)//2, 10.0)

left_score = 0
right_score = 0

# set the 'running' variable to False to end the game
running = True
# start the game loop
while running:
    # keep the loop running at the right speed
    clock.tick(FPS)
    # Game loop part 1: Events #####
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            pygame.quit()
        # add any other events here (keys, mouse, etc.)
    keys = pygame.key.get_pressed()  # checking pressed keys to move paddles
    if keys[pygame.K_UP]:
        right_paddle.move_up()
    if keys[pygame.K_DOWN]:
        right_paddle.move_down()
    if keys[pygame.K_w]:
        left_paddle.move_up()
    if keys[pygame.K_s]:
        left_paddle.move_down()

    # Game loop part 2: Updates #####
    # updating the ball's location
    ball.x += ball.x_speed
    ball.y += ball.y_speed
    if ball.y - ball.radius < PLAY_HEIGHT[0] or ball.y + ball.radius > PLAY_HEIGHT[1]:  # bouncing off the top and bottom
        ball.y_speed *= -1

    # handles the ball bounding off the paddles
    if (
            (ball.x + ball.radius > left_paddle.x > ball.x - ball.radius and  # ball's width overlaps the left paddle
            ball.y + ball.radius > left_paddle.y - PADDLE_HEIGHT//2 and  # ball is below the top of the left paddle
            ball.y - ball.radius < left_paddle.y + PADDLE_HEIGHT//2)  # ball is above the bottom of the left paddle
        or
            (ball.x- ball.radius < right_paddle.x - PADDLE_WIDTH < ball.x + ball.radius and  # ball's width overlaps the right paddle
            ball.y + ball.radius > right_paddle.y - PADDLE_HEIGHT // 2 and  # ball is below the top of the right paddle
            ball.y - ball.radius < right_paddle.y + PADDLE_HEIGHT // 2)  # ball is above the bottom of the right paddle
        ):
        ball.x_speed *= -1.2  # Ball's speed increases each time it bounces off a paddle, makes the game fun

        # if a ball hit's a moving paddle the ball's vertical movement is increased in the paddle's direction
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            ball.y_speed -= 3
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            ball.y_speed += 3

    # Checking if the ball has moving beyond the paddles into a scoring area
    elif ball.x < PLAY_WIDTH[0]:  # right player scores
        right_score += 1
        ball.reset(sum(PLAY_WIDTH)//2, sum(PLAY_HEIGHT)//2)
    elif ball.x > PLAY_WIDTH[1]:  # left player scores
        left_score += 1
        ball.reset(sum(PLAY_WIDTH) // 2, sum(PLAY_HEIGHT) // 2)

    # Game loop part 3: Draw #####
    screen.fill(BGCOLOR)
    # drawing the paddles and ball
    pygame.draw.rect(screen, WHITE, left_paddle.get_rect())
    pygame.draw.rect(screen, WHITE, right_paddle.get_rect())
    pygame.draw.circle(screen, WHITE, (ball.x, ball.y), ball.radius)

    # updating the scores
    left_score_img = font.render(str(left_score), True, WHITE)
    screen.blit(left_score_img, (10, 10))
    right_score_img = font.render(str(right_score), True, WHITE)
    screen.blit(right_score_img, (750, 10))

    pygame.draw.line(screen, WHITE, (PLAY_WIDTH[0] - PADDLE_WIDTH, PLAY_HEIGHT[0]), (PLAY_WIDTH[1], PLAY_HEIGHT[0]))  # top line
    pygame.draw.line(screen, WHITE, (PLAY_WIDTH[0] - PADDLE_WIDTH, PLAY_HEIGHT[1]), (PLAY_WIDTH[1], PLAY_HEIGHT[1]))  # bottom line
    # after drawing, flip the display
    pygame.display.flip()

# close the window
pygame.quit()
