import pygame
import sys
import components.components as components
from components.config import config, flags


# pygame instance
pygame.init()
pygame.display.set_caption("PONG by Mitch Embry")
clock = pygame.time.Clock()
# create screen
screen = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption("PONG by Mitch Embry")


def create_screen():
    screen.fill(config.black)

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

# game setup
def game_setup_loop():
    while not flags.playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_m:
                    flags.multiplayer = True
                    game_setup.difficulty()
                if event.key == pygame.K_RETURN:
                    game_setup.difficulty()
                if event.key == pygame.K_1:
                    flags.difficulty = "easy"
                    flags.playing = True
                if event.key == pygame.K_2:
                    flags.difficulty = 'medium'
                    flags.playing = True
                if event.key == pygame.K_3:
                    flags.difficulty = "hard"
                    flags.playing = True       
                
        pygame.display.flip()
        clock.tick(120)

    # setup second paddle to be AI or human and set paddle difficulty
    if not flags.multiplayer: 
        global p2_paddle
        p2_paddle = components.AiPaddleController(p2_paddle)
        p2_paddle.set_difficulty(flags.difficulty)


    else:
        p2_paddle = p2_paddle


    # set ball difficulty
    ball.set_difficulty(flags.difficulty)

def game_play_loop():
    while not flags.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
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
        flags.game_over = titles.win()
    
        pygame.display.flip()
        clock.tick(120)

def reset_flags():
    flags.running=True,
    flags.playing=False,
    flags.multiplayer=False,
    flags.game_over=False,
    flags.difficulty=None,


def game_over_loop():
    while flags.game_over:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        create_screen()
                        game_setup.intro()
                        reset_flags()

        pygame.display.flip()
        clock.tick(120)


def main_loop():
    while flags.running:  
        game_setup_loop()
        game_play_loop()
        game_over_loop()

main_loop()
