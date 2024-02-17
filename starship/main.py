import time
import curses

from animations import fire, animate_spaceship, run_spaceship
from drawing_tools import create_stars
from curses_tools import get_max_stars_count, Canvas
from space_garbage import fill_orbit_with_garbage
from settings import GARBAGE_COROUTINES, FIRE_SHOTS_COROUTINES, \
    ROCKET_COROUTINES
from spaceship import Spaceship

TIC_TIMEOUT = 0.1 * 1


def draw_border(canvas):
    """Draws border"""
    canvas.border()


def draw(canvas):
    """Draws blinking stars and flying starship"""
    stars_count = 3
    border_width = 1
    garbage_count = 3
    spaceship = Spaceship(
        'frames/rocket_frame_1.txt',
        'frames/rocket_frame_2.txt'
    )

    #window = Canvas(canvas)

    #determine_canvas_max_size(canvas)
    max_stars_count = get_max_stars_count(canvas)
    stars_count = min(stars_count, max_stars_count)

    stars_coroutines = create_stars(
        canvas,
        stars_count,
        border_width=border_width
    )

    spaceship_coroutine = run_spaceship(
        canvas=canvas, spaceship=spaceship,
        border_width=border_width
    )

    fill_orbit_with_garbage_coroutine = fill_orbit_with_garbage(
        canvas,
        garbage_count
    )

    tics = 0

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

        for coroutine in ROCKET_COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                ROCKET_COROUTINES.remove(coroutine)

        spaceship_coroutine.send(None)

        #canvas.addstr(15, 5, 'WOWcc' + str(tics), curses.A_DIM)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)
        tics += 1


def run_starship():
    curses.update_lines_cols()
    curses.wrapper(draw_border)
    curses.wrapper(draw)
    curses.curs_set(False)


if __name__ == '__main__':
    run_starship()
