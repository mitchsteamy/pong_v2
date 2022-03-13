import pygame
from .config import config

# TODO: difficulty is broken
# TODO: scoreboard for AI dude is broken

class Ball:
    def __init__(self, screen, color, x_pos, y_pos, rad, p1_paddle, p2_paddle):
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = -5
        self.y_vel = 0
        self.rad = rad
        self.p1_paddle = p1_paddle
        self.p2_paddle = p2_paddle

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x_pos, self.y_pos), self.rad)

    def move(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def bounce(self):
        if (self.x_pos + self.x_vel < self.p2_paddle.x_pos + self.p2_paddle.width) and (
            self.p2_paddle.y_pos
            < self.y_pos + self.y_vel + self.rad
            < self.p2_paddle.y_pos + self.p2_paddle.height + self.rad
        ):
            self.x_vel = -self.x_vel
            self.y_vel = (
                self.p2_paddle.y_pos + self.p2_paddle.height / 2 - self.y_pos
            ) / 15  # test
            self.y_vel = -self.y_vel
        elif self.x_pos + self.x_vel < 0:
            self.p1_paddle.score += 1
            self.x_pos = config.width / 2
            self.y_pos = config.height / 2
            self.x_vel = self.x_vel
            self.y_vel = 0
        if (self.x_pos + self.x_vel > self.p1_paddle.x_pos - self.p1_paddle.width) and (
            self.p1_paddle.y_pos
            < self.y_pos + self.y_vel + self.rad
            < self.p1_paddle.y_pos + self.p1_paddle.height + self.rad
        ):
            self.x_vel = -self.x_vel
            self.y_vel = (
                self.p1_paddle.y_pos + self.p1_paddle.height / 2 - self.y_pos
            ) / 15
            self.y_vel = -self.y_vel
        elif self.x_pos + self.x_vel > config.width:
            self.p2_paddle.score += 1
            self.x_pos = config.width / 2
            self.y_pos = config.height / 2
            self.x_vel = -self.x_vel
            self.y_vel = 0
        if self.y_pos + self.y_vel > config.height or self.y_pos + self.y_vel < 0:
            self.y_vel = -self.y_vel

    def set_x_vel(self, speed: int):
        self.x_vel = speed


class Paddle:
    def __init__(self, screen, color, x_pos, y_pos, width, height):
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.speed = -5
        self.score = 0
        self.state = "idle"

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


class AiPaddleController(Paddle):
    def __init__(self, paddle, ball, screen):
        self.score = 0
        self.speed = -4
        self.difficulty = "medium"  # TODO: use int enum settings
        self.paddle = paddle
        self.ball = ball
        self.screen = screen

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.paddle.set_speed(-1)
            self.ball.set_x_vel(-3)
        elif difficulty == "hard":
            self.paddle.set_speed(-8)
            self.ball.set_x_vel(-8)
        else:
            self.paddle.set_speed(-4)
            self.ball.set_x_vel(-4)

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
    def __init__(self, screen, p1_paddle, p2_paddle):
        self.game_font = pygame.font.SysFont("Ubuntu", 50)
        self.screen = screen
        self.p1_paddle = p1_paddle
        self.p2_paddle = p2_paddle

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


class GameSetupTitles:
    def __init__(self, screen):
        self.screen = screen
        self.game_font = pygame.font.SysFont("Ubuntu", 40)
        self.game_font_med = pygame.font.SysFont("Ubuntu", 30)
        self.game_font_small = pygame.font.SysFont("Ubuntu", 20)

        self.intro()

    def intro(self):
        self.screen.fill(config.black)
        self.intro = self.game_font_med.render(
            f"Press M for Multiplayer Mode. Press ENTER for Singleplayer.",
            False,
            config.white,
        )
        self.screen.blit(self.intro, (config.width // 25, config.height // 2 - 70))

    def difficulty(self):
        self.screen.fill(config.black)
        self.difficulty = self.game_font_med.render(
            f"Press 1 for Easy, 2 for Medium, or 3 for Hard.", False, config.white
        )
        self.screen.blit(self.difficulty, (config.width // 7, config.height // 2 - 70))

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
    def __init__(self, screen, p1_paddle, p2_paddle):
        self.screen = screen
        self.game_font = pygame.font.SysFont("Ubuntu", 40)
        self.game_font_med = pygame.font.SysFont("Ubuntu", 30)
        self.game_font_small = pygame.font.SysFont("Ubuntu", 20)
        self.p1_paddle = p1_paddle
        self.p2_paddle = p2_paddle

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
        if self.p1_paddle.score >= 10:
            self.screen.fill(config.black)
            self.screen.blit(self.p1_win, (config.width // 4, config.height // 2 - 85))
            self.screen.blit(
                self.play_again, (config.width // 6, config.height // 2 - 40)
            )
            
            self.p1_paddle.y_pos = config.height // 2 - self.p1_paddle.height // 2
            self.p2_paddle.y_pos = config.height // 2 - self.p1_paddle.height // 2
            playing = False
            return playing

        elif self.p2_paddle.score >= 10:
            self.screen.fill(config.black)
            self.screen.blit(self.p2_win, (config.width // 4, config.height // 2 - 85))
            self.screen.blit(
                self.play_again, (config.width // 6, config.height // 2 - 40)
            )
            self.p1_paddle.y_pos = config.height // 2 - self.p1_paddle.height // 2
            self.p2_paddle.y_pos = config.height // 2 - self.p1_paddle.height // 2
            playing = False
            return playing

        else:
            playing = True
            return playing
