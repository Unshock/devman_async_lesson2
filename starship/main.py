import time
import curses

from animations import run_spaceship, show_fire_alarm
from tools.drawing_tools import create_stars
from tools.curses_tools import Window
from space_garbage import fill_orbit_with_garbage
from settings.game_state import GARBAGE_COROUTINES, FIRE_SHOTS_COROUTINES
from settings import settings, game_state
from spaceship import Spaceship
from game_scenario import year_timer, show_year, show_phrase


def draw_border(canvas):
    """Draws border"""
    canvas.border()


def draw(canvas):
    """Draws blinking stars and flying starship"""
    derwin_bottom_indent = 4

    window = Window(canvas)

    derived_canvas = canvas.derwin(window.rows - derwin_bottom_indent, 0)
    derived_window = Window(derived_canvas)

    spaceship = Spaceship(
        window,
        *settings.SPACESHIP_FRAMES
    )

    stars_coroutines = create_stars(
        canvas,
        border_width=settings.BORDER_WIDTH,
        fullness=settings.STARS_FULLNESS
    )

    spaceship_coroutine = run_spaceship(
        window=window,
        spaceship=spaceship,
        border_width=settings.BORDER_WIDTH
    )

    fill_orbit_with_garbage_coroutine = fill_orbit_with_garbage(window)

    show_fire_alarm_coroutine = show_fire_alarm(window)

    game_is_not_over_coroutines = [
        year_timer(tics_for_year=settings.YEAR_TICS),
        show_year(window=derived_window),
        show_phrase(window=derived_window, tics_for_year=settings.YEAR_TICS),
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

        for coroutine in game_is_not_over_coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                game_is_not_over_coroutines.remove(coroutine)

        if game_state.YEAR >= settings.GUN_APPEARANCE_YEAR\
                and show_fire_alarm_coroutine:
            try:
                show_fire_alarm_coroutine.send(None)
            except StopIteration:
                show_fire_alarm_coroutine = None

        canvas.refresh()
        derived_canvas.refresh()
        time.sleep(settings.TIC_TIMEOUT)


def run_starship():
    curses.update_lines_cols()
    curses.wrapper(draw_border)
    curses.curs_set(False)
    curses.wrapper(draw)


if __name__ == '__main__':
    run_starship()
