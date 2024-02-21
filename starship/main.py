import time
import curses

from starship.animations import run_spaceship, show_fire_alarm
from starship.obstacles import show_obstacles
from starship.tools.drawing_tools import create_stars
from starship.tools.curses_tools import Window
from starship.space_garbage import fill_orbit_with_garbage
from starship.settings import settings, game_state
from starship.spaceship import Spaceship
from starship.game_scenario import run_game_scenario


def draw_border(canvas):
    """Draws border"""
    canvas.border()


def draw(canvas):
    """Draws blinking stars and flying starship"""
    derwin_bottom_indent = 4

    window = Window(canvas)

    derived_canvas = canvas.derwin(window.rows - derwin_bottom_indent, 0)
    derived_window = Window(derived_canvas)

    spaceship = Spaceship(window, *settings.SPACESHIP_FRAMES)

    create_stars(canvas, settings.STARS_FULLNESS, settings.BORDER_WIDTH)
    run_game_scenario(derived_window)

    coroutines = [
        fill_orbit_with_garbage(window),
        show_fire_alarm(window),
        run_spaceship(window, spaceship, settings.BORDER_WIDTH),
    ]

    game_state.coroutines += coroutines

    if settings.SHOW_OBSTACLES:
        game_state.coroutines.append(
            show_obstacles(canvas, game_state.OBSTACLES)
        )

    while True:

        for coroutine in game_state.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                game_state.coroutines.remove(coroutine)

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
