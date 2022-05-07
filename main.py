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

score = components.ScoreBoard(screen, p1_paddle, p2_paddle, ball)
titles = components.Titles(screen, p1_paddle, p2_paddle)

def create_screen():
    screen.fill(config.black)

create_screen()

# game setup
def game_setup_loop(titles):
    game_titles = titles
    game_titles.intro()

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
                    game_titles.input_difficulty()
                if event.key == pygame.K_RETURN:
                    flags.multiplayer = False
                    game_titles.input_difficulty()
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

def game_play_loop(screen, p1_paddle, p2_paddle, ball, titles, score):
    game_screen = screen
    player_1 = p1_paddle
    player_2 = p2_paddle
    game_ball = ball
    game_titles = titles
    game_score = score

    if not flags.multiplayer:
        player_2 = components.AiPaddleController(player_2)
        player_2.set_difficulty(flags.difficulty)
    
    else:
        player_2 = player_2

    # set ball difficulty
 
    game_ball.set_difficulty(flags.difficulty)

    #reset titles
    del game_titles
    game_titles = components.Titles(game_screen, player_1, player_2)
    
    # create scoreboard
    del game_score
    game_score = components.ScoreBoard(game_screen, player_1, player_2, game_ball)
    
    while flags.playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_w:
                    player_2.state = "up"
                if event.key == pygame.K_s:
                    player_2.state = "down"
                if event.key == pygame.K_UP:
                    player_1.state = "up"
                if event.key == pygame.K_DOWN:
                    player_1.state = "down"
            if event.type == pygame.KEYUP:
                player_1.state = "idle"
                player_2.state = "idle"

        create_screen()

        game_ball.draw()
        game_ball.bounce()
        game_ball.move()
        
        player_1.draw()
        player_1.move()

        player_2.draw()
        player_2.move()

        game_score.draw()
        game_score.score()

        flags.game_over = game_titles.win()
        flags.playing = not game_titles.win()
    
        pygame.display.flip()
        clock.tick(120)

def game_over_loop(titles):
    game_titles = titles
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
                        game_titles.intro()
                        flags.setup_mode = True
                        flags.game_over = False


        pygame.display.flip()
        clock.tick(120)

def reset_game(p1_paddle, p2_paddle, ball, titles, score):

    flags.playing = False
    flags.multiplayer = False
    flags.game_over = False
    flags.difficulty = None
    p1_paddle.score = 0
    p2_paddle.score = 0

    del ball
    ball = components.Ball(
        screen,
        config.white,
        config.width // 2,
        config.height // 2,
        config.line_weight * 2,
        )

    del p1_paddle
    p1_paddle = components.Paddle(
        screen,
        config.blue,
        (config.width - 20),
        (config.height // 2 - 10 * config.line_weight),
        2 * config.line_weight,
        20 * config.line_weight,
        ball
    )

    del p2_paddle
    p2_paddle = components.Paddle(
        screen,
        config.red,
        10,
        (config.height // 2 - 10 * config.line_weight),
        2 * config.line_weight,
        20 * config.line_weight,
        ball
    )     
    del titles
    titles = components.Titles(screen, p1_paddle, p2_paddle)

    del score
    score = components.ScoreBoard(screen, p1_paddle, p2_paddle, ball)

def main_loop():
    while flags.running:  
        game_setup_loop(titles)
        game_play_loop(screen, p1_paddle, p2_paddle, ball, titles, score)
        game_over_loop(titles)
        reset_game(p1_paddle, p2_paddle, ball, titles, score)

main_loop()
