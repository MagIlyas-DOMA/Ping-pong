import pygame
from random import randint
from screeninfo import get_monitors
from typing import Union, Literal
from dataclasses import dataclass

IF = Union[int, float]


def rand() -> int:
    i = randint(0, 1)
    return -1 if i == 0 else 1


def get_resolution():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height


def one_return(count: int, value=None):
    if count == 1:
        return value
    else:
        output = list()
        for i in range(count):
            output.append(value)
        return tuple(output)


def intlist(input: list) -> list:
    for i in range(len(input)):
        input[i] = int(input[i])
    return input


def int_float_separate(input: float, is_tuple: bool = False, is_int: bool = False):
    int_and_float = str(input).split('.')
    if is_int:
        int_and_float = intlist(int_and_float)
    if is_tuple:
        int_and_float = tuple(int_and_float)
    return int_and_float


def true_chance(chance: IF):
    b = int(1 / (chance / 100))
    rand = randint(1, b)
    return rand == b


def round_to_int(number: IF):
    return int(round(number, 0))


def if_dict_key(dct: dict, key):
    try:
        if dct[key]:
            pass
    except KeyError:
        return False
    else:
        return True


def dict_key_default(dct: dict, key, default):
    return default if not if_dict_key(dct, key) else dct[key]


def hd_textures(texture_type: Literal['hd', 'sd', 'ld'] = 'hd'):
    @dataclass
    class Paths:
        wood_block: str
        gold_block: str
        blue_block: str
        background: str
        game_over: str
        win: str

    wb = f'files/textures/blocks/{texture_type}/wood_block.png'
    gb = f'files/textures/blocks/{texture_type}/gold_block.png'
    bb = f'files/textures/blocks/{texture_type}/blue_block.png'
    bg = f'files/textures/background/{texture_type}.png'
    go = f'files/textures/game-over/{texture_type}.png'
    win = f'files/textures/win/{texture_type}.png'

    return Paths(wb, gb, bb, bg, go, win)


def full_screen(path):
    image = pygame.image.load(path) if type(path) is str else path
    return pygame.transform.scale(image, get_resolution())
