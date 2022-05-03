import pygame
from .config import config, flags

# TODO create play again feature

class Ball:
    def __init__(self, screen, color, x_pos, y_pos, rad):
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = 5
        self.y_vel = 0
        self.rad = rad

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x_pos, self.y_pos), self.rad)

    def move(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def bounce(self):
        if self.y_pos + self.y_vel > config.height or self.y_pos + self.y_vel < 0:
            self.y_vel = -self.y_vel

    def set_x_vel(self, new_x_vel: int):
        self.x_vel = new_x_vel
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.set_x_vel(4)
        elif difficulty == "hard":
            self.set_x_vel(7)
        else:
            self.set_x_vel(5)



class Paddle:
    def __init__(self, screen, color, x_pos, y_pos, width, height, ball):
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.ball = ball
        self.speed = - 5
        self.score = 0
        self.state = "idle"
        self.difficulty = "medium"

    def draw(self):
        pygame.draw.rect(
            self.screen, self.color, (self.x_pos, self.y_pos, self.width, self.height)
        )

    def move(self):
        if self.state == "up":
            self.y_pos += self.speed
        elif self.state == "down":
            self.y_pos += -self.speed
        if self.y_pos <= 0:
            self.y_pos = 0
        if self.y_pos >= config.height - self.height:
            self.y_pos = config.height - self.height


    def set_speed(self, speed: int):
        self.speed = speed

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.set_speed(-3)
        elif difficulty == "hard":
            self.set_speed(-6)
        else:
            self.set_speed(-4)
    



class AiPaddleController(Paddle):
    def __init__(self, paddle):
        self.paddle = paddle
        super().__init__(paddle.screen, paddle.color, paddle.x_pos, paddle.y_pos, paddle.width, paddle.height, paddle.ball)
    
    def draw(self):
        pygame.draw.rect(
            self.screen, self.paddle.color, (self.paddle.x_pos, self.paddle.y_pos, self.paddle.width, self.paddle.height)
        )

    def move(self):
        if (
            self.paddle.y_pos + self.paddle.height - 10 < self.ball.y_pos
            and self.ball.x_vel < 0
            and self.ball.x_pos < config.width // 2
        ):
            self.paddle.y_pos -= self.speed
        elif (
            self.paddle.y_pos > self.ball.y_pos
            and self.ball.x_vel < 0
            and self.ball.x_pos < config.width // 2
        ):
            self.paddle.y_pos += self.speed

        if self.paddle.y_pos <= 0:
            self.paddle.y_pos = 0
        if self.paddle.y_pos >= config.height - self.paddle.height:
            self.paddle.y_pos = config.height - self.paddle.height


class ScoreBoard:
    def __init__(self, screen, paddle_1, paddle_2, ball):
        self.game_font = pygame.font.SysFont("Ubuntu", 50)
        self.screen = screen
        self.p1_paddle = paddle_1
        self.p2_paddle = paddle_2
        self.ball = ball

    def draw(self):
        pygame.draw.line(
            self.screen,
            config.white,
            (config.width // 2, 0),
            (config.width // 2, config.height),
            2,
        )

        # draw score board
        self.score_1 = self.game_font.render(
            f"{str(self.p1_paddle.score)}", False, config.blue
        )
        self.score_2 = self.game_font.render(
            f"{str(self.p2_paddle.score)}", False, config.red
        )
        self.screen.blit(self.score_2, ((config.width // 2) - 60, config.height // 20))
        self.screen.blit(self.score_1, ((config.width // 2) + 28, config.height // 20))

    def score(self):
        if (self.ball.x_pos + self.ball.x_vel < self.p2_paddle.x_pos + self.p2_paddle.width) and (self.p2_paddle.y_pos < self.ball.y_pos + self.ball.y_vel < self.p2_paddle.y_pos + self.p2_paddle.height + self.ball.rad):
            self.ball.x_vel = -self.ball.x_vel
            self.ball.y_vel = (self.p2_paddle.y_pos + self.p2_paddle.height / 2 - self.ball.y_pos )/15 #test
            self.ball.y_vel = -self.ball.y_vel
        elif self.ball.x_pos + self.ball.x_vel < 0:
            self.p1_paddle.score += 1
            self.ball.x_pos = config.width / 2
            self.ball.y_pos = config.height / 2
            self.ball.x_vel = self.ball.x_vel
            self.ball.y_vel = 0
        if (self.ball.x_pos + self.ball.x_vel > self.p1_paddle.x_pos) and (self.p1_paddle.y_pos < self.ball.y_pos + self.ball.y_vel  < self.p1_paddle.y_pos + self.p1_paddle.height + self.ball.rad):
            self.ball.x_vel = -self.ball.x_vel
            self.ball.y_vel = (self.p1_paddle.y_pos + self.p1_paddle.height / 2 - self.ball.y_pos )/ 15 #test
            self.ball.y_vel = -self.ball.y_vel
        elif self.ball.x_pos + self.ball.x_vel > config.width:
            self.p2_paddle.score += 1
            self.ball.x_pos = config.width / 2
            self.ball.y_pos = config.height / 2
            self.ball.x_vel = - self.ball.x_vel
            self.ball.y_vel = 0
        

class GameSetupTitles:
    def __init__(self, screen):
        self.screen = screen
        self.game_font = pygame.font.SysFont("Ubuntu", 40)
        self.game_font_med = pygame.font.SysFont("Ubuntu", 30)
        self.game_font_small = pygame.font.SysFont("Ubuntu", 20)

    def instructions(self):
        self.screen.fill(config.black)
        self.instruction_1 = self.game_font_med.render(
            f"Player 1 use Up & Dowm keys. Player 2 use W & S Keys.",
            False,
            config.white,
        )
        self.instruction_2 = self.game_font_small.render(
            f"Press Space bar to begin Playing", False, config.white
        )
        self.screen.blit(
            self.instruction_1, (config.width // 15, config.height // 2 - 70)
        )
        self.screen.blit(
            self.instruction_2, (config.width // 3, config.height // 2 - 20)
        )


class Titles:
    def __init__(self, screen, paddle_1, paddle_2):
        self.screen = screen
        self.game_font = pygame.font.SysFont("Ubuntu", 40)
        self.game_font_med = pygame.font.SysFont("Ubuntu", 30)
        self.game_font_small = pygame.font.SysFont("Ubuntu", 20)
        self.paddle_1 = paddle_1
        self.paddle_2 = paddle_2

        self.intro()

    def intro(self):
        self.screen.fill(config.black)
        self.intro_text = self.game_font_med.render(
            f"Press M for Multiplayer Mode. Press ENTER for Singleplayer.",
            False,
            config.white,
        )
        self.screen.blit(self.intro_text, (config.width // 25, config.height // 2 - 70))

    def difficulty(self):
        self.screen.fill(config.black)
        self.difficulty_text = self.game_font_med.render(
            f"Press 1 for Easy, 2 for Medium, or 3 for Hard.", False, config.white
        )
        self.screen.blit(self.difficulty_text, (config.width // 7, config.height // 2 - 70))


    def win(self):
        self.p1_win = self.game_font.render(
            f"Player 1 is the winner.", False, config.blue
        )
        self.p2_win = self.game_font.render(
            f"Player 2 is the winner.", False, config.red
        )
        self.play_again = self.game_font_small.render(
            f"                    Press the space bar to play again",
            False,
            config.white,
        )
        
        if self.paddle_1.score >= 3:
            game_over = True
            
            self.screen.fill(config.black)
            self.screen.blit(self.p1_win, (config.width // 4, config.height // 2 - 85))
            self.screen.blit(self.play_again, (config.width // 6, config.height // 2 - 40))
            
            self.paddle_1.y_pos = config.height // 2 - self.paddle_1.height // 2
            self.paddle_2.y_pos = config.height // 2 - self.paddle_2.height // 2
            
            return game_over

        elif self.paddle_2.score >= 3:
            game_over = True

            self.screen.fill(config.black)
            self.screen.blit(self.p2_win, (config.width // 4, config.height // 2 - 85))
            self.screen.blit(self.play_again, (config.width // 6, config.height // 2 - 40))

            self.paddle_1.y_pos = config.height // 2 - self.paddle_1.height // 2
            self.paddle_2.y_pos = config.height // 2 - self.paddle_2.height // 2
            
            return game_over

        else:

            game_over = False
            return game_over


