import time
import curses

from animations import fire, animate_spaceship
from drawing_tools import create_stars
from curses_tools import get_max_stars_count
from space_garbage import fill_orbit_with_garbage
from settings import GARBAGE_COROUTINES, FIRE_SHOTS_COROUTINES
TIC_TIMEOUT = 0.1 * 1


def draw_border(canvas):
    """Draws border"""
    canvas.border()


def draw(canvas):
    """Draws blinking stars and flying starship"""
    stars_count = 150
    starship_speed = 1 * 2
    border_width = 1
    garbage_count = 3

    max_stars_count = get_max_stars_count(canvas)
    stars_count = min(stars_count, max_stars_count)

    stars_coroutines = create_stars(
        canvas,
        stars_count,
        border_width=border_width
    )

    spaceship_coroutine = animate_spaceship(
        canvas,
        border_width=border_width,
        speed=starship_speed
    )

    fill_orbit_with_garbage_coroutine = fill_orbit_with_garbage(
        canvas,
        garbage_count
    )

    while True:

        fill_orbit_with_garbage_coroutine.send(None)

        for coroutine in stars_coroutines.copy():
            coroutine.send(None)

        for coroutine in GARBAGE_COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                GARBAGE_COROUTINES.remove(coroutine)

        for coroutine in FIRE_SHOTS_COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                FIRE_SHOTS_COROUTINES.remove(coroutine)

        spaceship_coroutine.send(None)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def run_starship():
    curses.update_lines_cols()
    curses.wrapper(draw_border)
    curses.wrapper(draw)
    curses.curs_set(False)


if __name__ == '__main__':
    run_starship()
