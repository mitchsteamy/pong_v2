from dataclasses import dataclass


@dataclass
class PongConfig:
    white: tuple
    black: tuple
    red: tuple
    blue: tuple
    height: int
    width: int
    line_weight: int


config = PongConfig(
    white=(255, 255, 255),
    black=(0, 0, 0),
    red=(200, 56, 49),
    blue=(65, 105, 225),
    height=800,
    width=1000,
    line_weight=5,
)
