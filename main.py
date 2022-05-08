import pygame
import sys
import components.components as components
from components.config import config, flags


# pygame instance
pygame.init()
pygame.display.set_caption("PONG by Mitch Embry")

#create game clock
clock = pygame.time.Clock()

# create screen
screen = pygame.display.set_mode((config.width, config.height))


# Instatiation of objects
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

ai_paddle = components.AiPaddleController(p2_paddle)

score = components.ScoreBoard(screen, p1_paddle, p2_paddle, ball)

titles = components.Titles(screen, p1_paddle, p2_paddle)

def create_screen():
    screen.fill(config.black)

create_screen()

# game setup
def game_setup_loop(titles):

    setup_titles = titles
    setup_titles.intro()

    while flags.setup_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_m:
                    flags.multiplayer = True
                    setup_titles.input_difficulty()
                if event.key == pygame.K_RETURN:
                    flags.multiplayer = False
                    setup_titles.input_difficulty()
                if event.key == pygame.K_1:
                    flags.difficulty = "easy"
                    flags.playing = True
                    flags.setup_mode = False
                if event.key == pygame.K_2:
                    flags.difficulty = 'medium'
                    flags.playing = True
                    flags.setup_mode = False
                if event.key == pygame.K_3:
                    flags.difficulty = "hard"
                    flags.playing = True
                    flags.setup_mode = False
                       
        pygame.display.flip()
        clock.tick(120)

def game_play_loop(p1_paddle, p2_paddle, ai_paddle, ball, titles, score):

    game_p1 = p1_paddle
    game_ball = ball
    game_titles = titles
    game_score = score

    if not flags.multiplayer:
        game_p2 = ai_paddle
        game_p2.set_difficulty(flags.difficulty)
    
    else:
        game_p2 = p2_paddle

    # set ball difficulty
 
    game_ball.set_difficulty(flags.difficulty)

    #reset titles
    game_titles = titles
    
    # create scoreboard
    game_score = score
    
    while flags.playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_w:
                    game_p2.state = "up"
                if event.key == pygame.K_s:
                    game_p2.state = "down"
                if event.key == pygame.K_UP:
                    game_p1.state = "up"
                if event.key == pygame.K_DOWN:
                    game_p1.state = "down"
            if event.type == pygame.KEYUP:
                game_p1.state = "idle"
                game_p2.state = "idle"

        create_screen()

        game_ball.draw()
        game_ball.bounce()
        game_ball.move()
        
        game_p1.draw()
        game_p1.move()

        game_p2.draw()
        game_p2.move()

        game_score.draw()
        game_score.score()

        flags.game_over = True
        flags.playing = not game_titles.win()
    
        pygame.display.flip()
        clock.tick(120)

def game_over_loop(titles):

    over_titles = titles
    
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
                        over_titles.intro()
                        flags.setup_mode = True
                        flags.game_over = False


        pygame.display.flip()
        clock.tick(120)

def main_loop(screen, p1_paddle, p2_paddle, ai_paddle, ball, titles, score):
    
    main_screen = screen
    main_p1 = p1_paddle
    main_p2= p2_paddle
    ai_p2 = ai_paddle
    main_ball = ball
    main_titles = titles
    main_score = score

    while flags.running:  
        game_setup_loop(main_titles)
        game_play_loop (main_p1, main_p2, ai_p2, main_ball, main_titles, main_score)
        game_over_loop(main_titles)


        flags.playing = False
        flags.multiplayer = False
        flags.game_over = False
        flags.difficulty = None
        main_p1.score = 0
        main_p2.score = 0

    del main_screen
    main_screen = screen

    del main_p1
    main_p1 = p1_paddle

    del main_p2
    main_p2 = p2_paddle

    del main_ball
    main_ball = ball
    
    del main_titles
    main_titles = titles

    del main_score
    main_score = score

main_loop(screen, p1_paddle, p2_paddle, ai_paddle, ball, titles, score)
