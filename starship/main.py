import time
import curses

from animations import fire, animate_spaceship
from drawing_tools import create_stars
from curses_tools import get_max_stars_count

TIC_TIMEOUT = 0.1


def draw_border(canvas):
    """Draws border"""
    canvas.border()


def draw(canvas):
    """Draws blinking stars and flying starship"""
    stars_count = 150
    starship_speed = 1
    border_width = 1

    max_stars_count = get_max_stars_count(canvas)
    stars_count = min(stars_count, max_stars_count)

    max_y, max_x = canvas.getmaxyx()
    mid_row = max_y // 2
    mid_column = max_x // 2

    coroutines = create_stars(canvas, stars_count, border_width=border_width)

    fire_shot_coroutine = fire(
        canvas,
        start_row=mid_row,
        start_column=mid_column,
        rows_speed=-0.9
    )
    spaceship_coroutine = animate_spaceship(
        canvas,
        border_width=border_width,
        speed=starship_speed
    )

    coroutines += [fire_shot_coroutine, spaceship_coroutine]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(fire_shot_coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def run_starship():
    curses.update_lines_cols()
    curses.wrapper(draw_border)
    curses.curs_set(False)
    curses.wrapper(draw)


if __name__ == '__main__':
    run_starship()
