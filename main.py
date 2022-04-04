from logging.config import dictConfig
import pygame
import sys
import components.components as components
from components.config import config


# pygame instance
pygame.init()
pygame.display.set_caption("PONG by Mitch Embry")
clock = pygame.time.Clock()
# create screen
screen = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption("PONG by Mitch Embry")


def create_screen():
    screen.fill(config.black)

def reset_score():
        if playing == False:
            p1_paddle.score = 0
            p2_paddle.score = 0 

create_screen()

# ball and paddle instances
ball = components.Ball(
    screen,
    config.white,
    config.width // 2,
    config.height // 2,
    config.line_weight * 2,
)

p1_paddle = components.Paddle(
    screen,
    config.blue,
    (config.width - 20),
    (config.height // 2 - 10 * config.line_weight),
    2 * config.line_weight,
    20 * config.line_weight,
    ball
)

p2_paddle = components.Paddle(
    screen,
    config.red,
    10,
    (config.height // 2 - 10 * config.line_weight),
    2 * config.line_weight,
    20 * config.line_weight,
    ball
)



#scores and title instances
game_setup = components.GameSetupTitles(screen)
score = components.ScoreBoard(screen, p1_paddle, p2_paddle, ball)
titles = components.Titles(screen, p1_paddle, p2_paddle)

# main function
running = True
playing = False
multi_player_mode = False


# settings
difficulty = None

# game setup
while not playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_m:
                multi_player_mode = True
                game_setup.difficulty()
            if event.key == pygame.K_RETURN:
                game_setup.difficulty()
            if event.key == pygame.K_1:
                difficulty = "easy"
                playing = True
            if event.key == pygame.K_2:
                difficulty = 'medium'
                playing = True
            if event.key == pygame.K_3:
                difficulty = "hard"
                playing = True
        
            
    pygame.display.flip()
    clock.tick(120)

# setup second paddle to be AI or human and set paddle difficulty
if not multi_player_mode: 
   
    p2_paddle = components.AiPaddleController(p2_paddle)
    p2_paddle.set_difficulty(difficulty)


else:
    p2_paddle = p2_paddle


# set ball difficulty
ball.set_difficulty(difficulty)

# set score to zero
reset_score()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_SPACE:
                titles = components.Titles(screen, p1_paddle, p2_paddle)
            if event.key == pygame.K_w:
                p2_paddle.state = "up"
            if event.key == pygame.K_s:
                p2_paddle.state = "down"
            if event.key == pygame.K_UP:
                p1_paddle.state = "up"
            if event.key == pygame.K_DOWN:
                p1_paddle.state = "down"
        if event.type == pygame.KEYUP:
            p1_paddle.state = "idle"
            p2_paddle.state = "idle"

    create_screen()

    ball.draw()
    ball.bounce()
    ball.move()
    
    p1_paddle.draw()
    p1_paddle.move()

    p2_paddle.draw()
    p2_paddle.move()

    score.score()
    score.draw()
    playing  = titles.win()
    first_game = titles.win()
    
   
    pygame.display.flip()
    clock.tick(120)
