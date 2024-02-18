import time
import curses

from animations import run_spaceship
from tools.drawing_tools import create_stars
from tools.curses_tools import Window
from space_garbage import fill_orbit_with_garbage
from settings.game_state import GARBAGE_COROUTINES, FIRE_SHOTS_COROUTINES
from settings import settings
from spaceship import Spaceship
from game_scenario import year_timer, show_year, show_phrase


def draw_border(canvas):
    """Draws border"""
    canvas.border()


def draw(canvas):
    """Draws blinking stars and flying starship"""
    border_width = 1

    window = Window(canvas)

    derived_canvas = canvas.derwin(window.rows - 4, 0)
    derived_window = Window(derived_canvas)

    spaceship = Spaceship(
        window,
        'frames/rocket_frame_1.txt',
        'frames/rocket_frame_2.txt'
    )

    stars_coroutines = create_stars(
        canvas,
        border_width=border_width,
        fullness=0.05
    )

    spaceship_coroutine = run_spaceship(
        window=window,
        spaceship=spaceship,
        border_width=border_width
    )

    fill_orbit_with_garbage_coroutine = fill_orbit_with_garbage(window)

    year_timer_coroutine = year_timer(tics_for_year=settings.YEAR_TICS)
    show_year_coroutine = show_year(derived_window)
    phases_coroutine = show_phrase(
        window=derived_window,
        tics_for_year=settings.YEAR_TICS
    )

    game_coroutines = [
        year_timer_coroutine,
        show_year_coroutine,
        phases_coroutine,
        spaceship_coroutine
    ]

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

        for coroutine in game_coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                game_coroutines.remove(coroutine)

        canvas.refresh()
        derived_canvas.refresh()
        time.sleep(settings.TIC_TIMEOUT)


def run_starship():
    curses.update_lines_cols()
    curses.wrapper(draw_border)
    curses.wrapper(draw)
    curses.curs_set(False)


if __name__ == '__main__':
    run_starship()
