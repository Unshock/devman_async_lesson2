from random import choice, randint

from animations import blink


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


def create_stars(canvas, stars_count, border_width=1) -> list:
    """Creates list of stars coroutines without overlapping"""

    stars_list = []
    stars_coords = []

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
