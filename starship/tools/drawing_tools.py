from random import choice, randint

from starship.tools.curses_tools import get_max_stars_count
from starship.animations import blink


def get_random_star_coords(canvas, border_width=1) -> tuple:
    """Gets random star coord taking canvas size and border into account"""

    max_y, max_x = canvas.getmaxyx()
    return randint(border_width, max_y - border_width - 1), \
        randint(border_width, max_x - border_width - 1)


def get_random_star_icon() -> str:
    """Gets random icon for the blinking star"""

    icons = ['+', '*', '.', ':']
    return choice(icons)


def get_random_blink_delay(min_delay=1, max_delay=50) -> int:
    """Gets random blink delay for the star for async coroutines"""

    return randint(min_delay, max_delay)


def create_stars(canvas, fullness=0.1, border_width=1) -> list:
    """Creates list of stars coroutines without overlapping"""

    if fullness < 0 or fullness > 1:
        raise ValueError(
            f'Fullness parameter {fullness} is incorrect. '
            f'Must be in the range from 0 to 1.')

    stars_list = []
    stars_coords = []

    max_stars_count = get_max_stars_count(canvas)
    stars_count = int(max_stars_count * fullness)

    while len(stars_coords) < stars_count:
        row, col = get_random_star_coords(canvas, border_width=border_width)

        if (row, col) in stars_coords:
            continue

        stars_coords.append((row, col))

        icon = get_random_star_icon()
        delay = get_random_blink_delay()
        star_coroutine = blink(canvas, row, col, symbol=icon, delay=delay)
        stars_list.append(star_coroutine)

    return stars_list
